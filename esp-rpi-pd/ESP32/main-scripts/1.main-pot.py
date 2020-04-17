# This example demonstrates an analog sensor peripheral.
#
# The sensor's local value updates every second, and it will notify
# any connected central every 10 seconds.
import bluetooth
import random
import struct
import time
from ble_advertising import advertising_payload
from machine import Pin, ADC
from micropython import const

pot = ADC(Pin(32))
pot.atten(ADC.ATTN_11DB)

_IRQ_CENTRAL_CONNECT = const(1 << 0)
_IRQ_CENTRAL_DISCONNECT = const(1 << 1)

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.analog
_ANALOG_CHAR = (
    bluetooth.UUID(0x2A58),
    bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,
)
_ENV_SENSE_SERVICE = (
    _ENV_SENSE_UUID,
    (_ANALOG_CHAR,),
)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_UNKNOWN = const(0) # maybe change in the future

class BLEadc:
    def __init__(self, ble, name="mpy-adc"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(handler=self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_ENV_SENSE_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(
            name=name, services=[_ENV_SENSE_UUID], appearance=_ADV_APPEARANCE_UNKNOWN
        )
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _, = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _, = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()

    def set_adcVal(self, adcVal, notify=False):
        # Write the local value, ready for a central to read.
        self._ble.gatts_write(self._handle, struct.pack("<h", int(adcVal)))
        if notify:
            for conn_handle in self._connections:
                # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._handle)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)


def demo():
    ble = bluetooth.BLE()
    adc = BLEadc(ble)

    t = 25
    i = 0

    while True:
        pot_value = pot.read()
        # Write every second, notify every 10 seconds.
        i = (i + 1) % 10
        adc.set_adcVal(pot_value, notify=i == 0)
        time.sleep_ms(1000)


if __name__ == "__main__":
    demo()