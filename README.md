# BLE Passthrough

## 🛰️ BLE Raw Advertisement Events for Home Assistant

> 🔎 Capture all raw BLE advertisements (ADV packets) inside Home Assistant — from all Bluetooth adapters and proxies — and forward them as real-time HA events.

## 📘 Overview

This custom integration registers a passive BLE listener via `BluetoothCallbackMatcher(connectable=False)` to tap into **all incoming BLE advertisement packets**, regardless of their source or whether they are claimed by a Home Assistant integration.

## How to Install

1. Clone or copy this repository into your Home Assistant configuration under:

```arduino
<config>/custom_components/ble_passthrough/
```

2. Add the following to your configuration.yaml file:

```yaml
ble_passthrough:
```

3. Restart Home Assistant.

**Once restarted, the integration will begin listening for BLE advertisements automatically.**

📌 Note: This integration does not use UI configuration (config_flow: false), so it must be activated via YAML.


### ✅ Sources include:
- 🖥️ Local BlueZ-based adapters
- 📶 ESPHome Bluetooth Proxy devices
- 🌐 Remote Bluetooth Proxies via TCP/Socket
- 🧱 Any `bluetooth_proxy`-enabled adapter supported by HA

### 📡 Each raw advertisement is emitted as:

```python
hass.bus.async_fire(
    "ble_raw_advertisement",
    {
        "address": "AA:BB:CC:DD:EE:FF",
        "rssi": -67,
        "data": "0201061AFF99040512AABBCCDDEE",
        "source": "esp32-proxy-1234"
    }
)
```

## 📚 License

MIT License
