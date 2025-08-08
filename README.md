# BLE Passthrough

## 🛰️ BLE Raw Advertisement Events for Home Assistant

> 🔎 Capture all raw BLE advertisements (ADV packets) inside Home Assistant — from all Bluetooth adapters and proxies — and forward them as real-time HA events.

## 📘 Overview

This custom integration registers a passive BLE listener via `BluetoothCallbackMatcher(connectable=False)` to tap into **all incoming BLE advertisement packets**, regardless of their source or whether they are claimed by a Home Assistant integration.

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
