# Papouch integration

The **Papouch** integration allows you to integrate your [Papouch](https://papouch.com/) hardware devices into Home Assistant.

The integration works by continuously polling the device for real-time data and updating the corresponding Home Assistant entities. In addition to monitoring, it provides command entities to control the device outputs, and configuration entities to adjust hardware settings, such as counter modes and sensor types.

[![Open your Home Assistant instance and open a repository in the Marketplace.](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=VladislavLevitskii&repository=Papouch-custom-component)

For installation you can use the link above or you can:

1. Go to **Settings** > **Marketplace** > **Browse**
2. Search for **"Papouch"**

> **Note**:
> This integration requires Home Assistant version **2026.11** or newer.
> If you are running an older version, you can still install it via HACS.

## Supported devices

Currently, Ethernet devices in **WEB** and **TCP server** modes are supported:

- **Quido ETH** (Input/output modules)
- **TH2E** (Thermometers and environmental sensors)
- **TME** (Multi-channel thermometers)
  - **TME Multi / Radio**
- **Papago** (Ethernet sensors and meteo stations)
  - **Meteo**
  - **5HDI DO**
  - **2TH**
  - **TH 2DI DO**

and serial devices (via RS485):

- **Quido RS485**
- **THT2**
- **TQS4**
- **THCO2**

## Configuration

After adding our integration you will be asked to choose whether you want to add a network device, a network hub or a serial hub.

### Network device

The first step of adding a network device is an active discovery using broadcast:

#### Device discovery

All supported Papouch devices feature DHCP discovery. Once the integration is active in your Home Assistant instance, devices sending DHCP requests will automatically appear in the **Discovered** section on the Integrations page. Selecting **Configure** will guide you through the setup process.

> **Note:**
> This will be active if DHCP is enabled in the device. Note that devices with an active password configured may fail or be skipped during automatic DHCP discovery because authentication is required.

Active discovery is also triggered automatically when you manually add the integration via the user interface. It will scan your local network using UDP broadcasts and present a list of available, unregistered devices along with their names, locations, and IP addresses. However, if a device has a password set, it will not be displayed in the list of available devices during network scan.

> **Note:**
> If your Home Assistant instance is running in an isolated network environment (such as Windows Subsystem for Linux (WSL) or specific Docker network configurations) where UDP broadcasts cannot reach the container, automatic discovery will fail. In this case, you can simply select the option to enter the IP address manually during the configuration flow.

If your device was not discovered automatically, you can complete the setup manually by entering the IP address:

1. Enter the device's IP address, your preferred polling interval, HTTP port and the admin password (if set).
2. In the final step, you can assign the device to an area and customize its name.

> **Note:**
> If the device doesn't have any password set and you provide one in the setup, it will work; however, the reverse will fail if the device expects a password that is not provided.

> **Note:**
> Some devices can run in different modes, like TCP client or UDP. If you try to set up a device that is not in **WEB** or **TCP** mode, the integration will detect this and offer to switch it to **WEB** mode or abort the setup.

> **Note:**
> The device must be powered on and reachable by Home Assistant during the initial setup. The integration cannot be configured with an offline IP address because it needs to fetch the hardware configuration data to create a valid instance.

#### Reconfiguration

If your device's IP address or access password changes, you can update the integration settings without removing and re-adding the device:

1. Go to **Settings** > **Devices & services** and select the Papouch integration.
2. Select the three dots menu, then select **Reconfigure**.
3. You can update the IP address, password or HTTP port as needed.

> **Note:**
> The reconfiguration flow updates the connection credentials and IP address used by Home Assistant to communicate with the device. It does not modify the physical device's internal configuration (such as changing its IP address or password on the device itself).

> **Warning:**
> You can reconfigure a device only if the mode didn't change. Example: If a device was configured using e.g. TCP server mode and later you will change it to WEB mode and try to reconfigure it, the error will be raised. You need to manually change the mode mode back or just delete the entry and configure the device again.

#### Polling interval

After creating a configuration for a device, you can change its polling interval by:

1. Navigate to **Settings** > **Devices & Services**.
2. Click the cog icon right next to the three dots in your Papouch integration, enter a new polling interval, and click **Submit**.

### Serial device

When you choose to add a serial hub, you are asked to select a serial port, baudrate and scan interval. Note that if you can't see the port you want to communicate via, you can choose `Enter port manually` and don't forget to set proper permissions.

#### Serial hub

After successfully creating the hub you can manage it via Serial Hub Options (a cog near the three dots). There you can add new devices, remove them or change the scan interval.

##### Adding a device

There, you will be asked to add the device using its address (if you know it), its serial number, or via broadcast. Note that using broadcast requires having only one device connected to the bus.

>**Note**: Adding using serial number will change the device's address. (From the address 250 and going lower). Moreover the format of the serial number should be: 0123/4567.

>**Note**: Home Assistant doesn't remember your previously configured devices. It means that if you change the address using its serial number and then delete device's configuration, the configuration of the different device will assign the SAME address to a different device.

Adding a serial device doesn't show you the option to change its name and location, so you can do it by clicking on the `pen` icon.

#### Reconfiguration

As in the network branch you can manage the settings of the serial hub.

1. Go to **Settings** > **Devices & services**" and select the Papouch integration.
2. Select the three dots menu, then select **Reconfigure**.
3. You can update the serial port or baudrate if needed.

>**Note**: This reconfiguration option updates the parameters while preserving the existing config entry and any user-defined names.

### Network hub

A network hub represents converters that are connected using TCP and transmit incoming bytes directly to the bus. That's why the network hub option is similar to the serial hub, the only difference is that you need to select (or enter manually) an IP address instead of a port and enter HTTP port with the admin password. Other options like adding or removing the serial devices are completely the same. 

## Diagnostics

This integration supports Home Assistant diagnostics, allowing you to export technical details and configuration states to help troubleshoot issues. You can download the diagnostic data by:

1. Navigating to **Settings** > **Devices & Services**.
2. Finding your Papouch integration and clicking the three dots on the configuration entry.
3. Selecting **Download diagnostics**.

## Using the device

While the ethernet device's built-in web interface remains the primary place for core configuration, this integration exposes certain settings directly within Home Assistant for your convenience.

> **Important:**
> If you change settings directly via the device's web interface (if it has one), the integration will not automatically detect all of these changes. We highly recommend **reloading** the integration (Settings > Devices & Services > three dots > **Reload**) after making external changes to keep the states synchronized.

### Known limitations and nuances

This section describes various limitations and nuances that can occur while using the devices.

#### Number entities

When adjusting a `number` entity using the up/down arrows in the Home Assistant UI, every single step immediately sends a command to the device. To jump to a specific value without sending intermediate commands, type the exact number directly into the input field and press Enter.

#### Select entities

Select entities (such as counter modes or sensor types) are not continuously polled. If you change them directly on the device's web interface, Home Assistant will be unaware of the change until the integration is reloaded.

> **Warning:**
> Changing the operating mode via a `select` entity causes the physical (Ethernet) device to restart. For this reason, it is strongly advised **not** to use these select entities in automations.

#### Units of measurement

Changing the physical unit of measurement on the device's web interface will not automatically update the unit in Home Assistant. Doing so may also disrupt your long-term statistics and require you to fix the historical data manually.

#### Dynamic entities

Some devices (e.g., TH2E) expose a variable number of entities depending on the configured sensor type. If you change the sensor type, some previously active entities may become unavailable. You can safely delete these orphaned entities from Home Assistant; their historical data will remain intact, and they will be recreated if you ever switch the sensor type back. To recreate entities after changing hardware configurations, use a reload action (more details in [Troubleshooting](#troubleshooting)).

### Quido

The integration provides the following entities for Quido devices:

- **Binary sensor**: Watches the state of digital inputs.
- **Button**: Allows bulk connecting/disconnecting of all outputs and resetting counters.
- **Number**:
  - Decreasing counters by a specific value (up to 2<sup>32</sup> - 1).
  - Setting the output connection/disconnection duration (from 0.5s to 127.5s with 0.5s step).
- **Select**: Changes the operation mode of the input counters.
- **Sensor**: Reads temperature and pulse counts.
- **Switch**: Changes the state of individual outputs.

The official manual can be found in the downloads section of the [Quido product page](https://papouch.com/quido-eth-4-4-4-vstupy-4-vystupy-teplomer-ethernet-p4646/?cid=145&vid=1797).

### TH2E

The integration provides the following entities for TH2E device:

- **Button**: Triggers automatic configuration of the connected sensor type (triggers a restart).
- **Select**: Allows manual selection and configuration of the connected sensor type.
- **Sensor**: Provides environmental readings depending on the configured sensor type.

For more details, see the official manual available in the downloads section of the [TH2E product page](https://papouch.com/th2e-ethernetovy-teplomer-s-vlhkomerem-p4825/?vid=2374).

### THT2

The integration provides the following entity for THT2 device:

- **Sensor**: Provides environmental readings (temperature, humidity and dew point).

For more details, see the official manual available in the downloads section of the [THT2 product page](https://papouch.com/tht2-vlhkomer-a-teplomer-s-rs485-elektronika-p2204/).

### TQS 4

The integration provides the following entity for THT2 device:

- **Sensor**: Provides environmental readings (temperature).

For more details, see the official manual available in the downloads section of the [THT2 product page](https://papouch.com/tqs4-e-elektronika-teplomeru-s-rs485-p3623/).

### THCO2

The integration provides the following entity for THCO2 device:

- **Sensor**: Provides environmental readings (CO2 level, temperature, humidity and dew point).

For more details, see the official manual available in the downloads section of the [THT2 product page](https://papouch.com/thco2-senzor-koncentrace-co2-teplomer-a-vlhkomer-s-rs485-p5034/).

### TME / TME Multi / TME Radio

The integration provides the following entities for TME devices:

- **Sensor**: Provides environmental readings depending on the configured sensor type.

For more details, see the official manuals available in the downloads section of the [TME](https://papouch.com/tme-ethernetovy-teplomer-p4602/?sti=635677&vid=1879) and [TME Multi/Radio](https://papouch.com/tme-radio-bezdratovy-meric-teploty-a-vlhkosti-p4603/?sti=635678&vid=2965) product pages.

### Papago

Papago is a family of devices.

#### Meteo

The integration provides these entities:

- **Button**: Automatic type configuration of the sensor (only for sensors A and B, since sensor C has only 1 possible sensor type. This does not cause a restart).
- **Select**: Allows manual selection and configuration of the connected sensor type.
- **Sensor**: Various sensors depending on the type of the sensor.

The official manual can be found in the downloads section of the [Papago Meteo product page](https://papouch.com/papago-meteo-eth-zakladna-prumyslove-meteostanice-s-ethernetem-a-poe-p6878/?vid=4887).

#### 5HDI DO

The integration provides the following entities:

- **Binary sensor**: Watches the state of digital inputs.
- **Button**: Allows bulk connecting/disconnecting of all outputs and resetting counters.
- **Number**:
  - Decreasing counters by a specific value (up to 2<sup>32</sup> - 1).
  - Setting the output connection/disconnection duration (from 0.5s to 127.5s with 0.5s step).
- **Select**: Changes the operation mode of the input counters.
- **Sensor**: Reads temperature and pulse counts.
- **Switch**: Changes the state of individual outputs.

The official manual can be found in the downloads section of the [Papago 5HDI DO product page](https://papouch.com/papago-5hdi-do-eth-5-digitalni-vstup-a-1-rele-p3132/).

#### 2TH

The integration provides these entities:

- **Button**: Automatic type configuration of both sensors (does not cause a restart).
- **Sensor**: Various sensors depending on the type of the sensor.
- **Select**: Allows manual selection and configuration of the connected sensor type.

The official manual can be found in the downloads section of the [Papago 2TH product page](https://papouch.com/papago-2th-eth-2-mereni-teploty-vlhkosti-a-rosneho-bodu-s-ethernetem-p2989/).

#### TH 2DI DO

- **Binary sensor**: Watches the state of digital inputs.
- **Button**:
  - Allows bulk connecting/disconnecting of all outputs and resetting counters.
  - Automatic type configuration of both sensors (does not require a restart).
- **Number**:
  - Decreasing counters by a specific value (up to 2<sup>32</sup> - 1).
  - Setting the output connection/disconnection duration (from 0.5s to 127.5s with 0.5s step).
- **Select**:
  - Changes the operation mode of the input counters.
  - Allows manual selection and configuration of the connected sensor type.
- **Sensor**:
  - Reads temperature and pulse counts.
  - Various sensors depending on the type of the sensor.
- **Switch**: Changes the state of individual outputs.

The official manual can be found in the downloads section of the [Papago TH 2DI DO product page](https://papouch.com/papago-th-2di-do-eth-environment-monitor-p3159/).

## Troubleshooting

The integration detects supported sensors and outputs during its initial setup. If you change the physical configuration of your Papouch device (for example, plugging a new sensor into an empty port, or switching a port's operating mode between a thermometer and a hygrometer), the new entities will not appear automatically, and the old ones will not be removed.

To apply these hardware changes:

1. Make sure your device has fully restarted and is working with the new configuration.
2. Navigate to **Settings** > **Devices & Services**.
3. Click the three dots next to your Papouch integration and select **Reload**.

The integration will fetch the updated hardware layout and create the new entities. The old entity (e.g., the previous thermometer) will become `unavailable` and you can manually delete it from the Home Assistant entity registry. Thanks to MAC address/Serial number identification, you will not lose any historical data for the sensors that remained untouched.

## Support and Issues

If you encounter any bugs, issues, or have feature requests, please open an issue.