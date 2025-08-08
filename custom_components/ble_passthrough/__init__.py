from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED, EVENT_HOMEASSISTANT_STOP
from homeassistant.components.bluetooth import (
    async_register_callback,
    BluetoothCallbackMatcher,
    BluetoothChange,
    BluetoothScanningMode,
    BluetoothServiceInfoBleak,
)
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ble_passthrough"
EVENT_BLE_RAW_ADVERTISEMENT = "ble_passthrough.adv_received"


def setup(hass: HomeAssistant, config: dict):
    """Set up the BLE Raw Logger integration."""

    @callback
    def handle_ble_event(
        service_info: BluetoothServiceInfoBleak, change: BluetoothChange
    ):
        """Handle each BLE advertisement callback."""
        if change != BluetoothChange.ADVERTISEMENT:
            return

        address = service_info.address
        rssi = service_info.rssi
        raw = getattr(service_info, "raw", None)
        source = service_info.source

        hex_str = raw.hex() if raw else ""
        hex_bytes = [hex_str[i : i + 2].upper() for i in range(0, len(hex_str), 2)]

        _LOGGER.debug(
            "🔵 Received BLE ADV from %s, RSSI: %s, raw: %s, source: %s",
            address,
            rssi,
            hex_bytes,
            source,
        )

        hass.bus.async_fire(
            EVENT_BLE_RAW_ADVERTISEMENT,
            {"address": address, "rssi": rssi, "data": hex_bytes, "source": source},
        )

    @callback
    def start_listen_ble(event):
        """Start listening to BLE advertisements after HA is started."""
        _LOGGER.info("Registering BLE advertisement callback...")
        cancel = async_register_callback(
            hass,
            handle_ble_event,
            BluetoothCallbackMatcher(connectable=False),
            BluetoothScanningMode.PASSIVE,
        )

        hass.data[DOMAIN] = cancel
        _LOGGER.info("✅ BLE ADV callback registered successfully.")

    hass.data.setdefault(DOMAIN, None)
    hass.bus.listen_once(EVENT_HOMEASSISTANT_STARTED, start_listen_ble)

    @callback
    def _async_handle_stop(event: Event) -> None:
        """Cancel the callback."""
        cancel = hass.data.get(DOMAIN)
        if cancel:
            cancel()
            _LOGGER.info("🛑 BLE ADV callback cancelled.")

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _async_handle_stop)

    return True
