"""Initialization file of the integration."""

from typing import TYPE_CHECKING

import aiohttp
import homeassistant.helpers.config_validation as cv
from aiopapouch import PapouchHTTPClient, create_device
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import AUTH_FAILED_ERROR, DEFAULT_WEB_PORT
from .coordinator import PapouchDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.typing import ConfigType


DOMAIN = "papouch"
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]

type PapouchConfigEntry = ConfigEntry[PapouchDataUpdateCoordinator]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:  # noqa: ARG001
    """Set up. (Unused)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: PapouchConfigEntry) -> bool:
    """Set up Papouch device from a config entry."""
    session = async_get_clientsession(hass)
    password = entry.data.get("password", "")
    web_port = entry.data.get("web_port", DEFAULT_WEB_PORT)
    api_client = PapouchHTTPClient(
        entry.data["ip_address"], session, password=password, web_port=web_port
    )

    entry.async_on_unload(entry.add_update_listener(update_listener))

    device_ip_msg = f"Papouch device at {api_client.ip_address}"

    try:
        device = await create_device(api_client)
    except aiohttp.ClientResponseError as err:
        if err.status == AUTH_FAILED_ERROR:
            auth_err_msg = f"Invalid authentication for {device_ip_msg}, error: {err}"
            raise ConfigEntryAuthFailed(auth_err_msg) from err

        auth_err_msg = f"Failed to connect to {device_ip_msg}, error: {err}"
        raise ConfigEntryNotReady(auth_err_msg) from err
    except aiohttp.ClientError as err:
        auth_err_msg = f"Failed to connect to {device_ip_msg}, error: {err}"
        raise ConfigEntryNotReady(auth_err_msg) from err

    if device is None:
        id_err_msg = "Failed to identify device type"
        raise ConfigEntryNotReady(id_err_msg)

    if entry.unique_id is None and device.mac_address:
        hass.config_entries.async_update_entry(entry, unique_id=device.mac_address)

    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections={(dr.CONNECTION_NETWORK_MAC, device.mac_address)},
        identifiers={(DOMAIN, device.mac_address)},
        name=device.name,
        manufacturer=device.manufacturer,
        model=device.name,
        suggested_area=device.location,
    )

    coordinator = PapouchDataUpdateCoordinator(hass, api_client, entry, device)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: PapouchConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)
