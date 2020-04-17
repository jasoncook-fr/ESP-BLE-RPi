# This example shows the use of two values being sent in one handle
# A potentiometer and a button are used to send two different values
import bluetooth
import random
import struct
import time
from ble_advertising import advertising_payload
from machine import Pin, ADC
from micropython import const

pot = ADC(Pin(32))
pot.atten(ADC.ATTN_11DB)
button = Pin(39, Pin.IN)

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
            print("------ central disconnect -----")
            conn_handle, _, _, = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()

    def set_adcVal(self, adcVal, buttonVal, notify=False):
        # Write the local value, <h for short val (2 bytes: for pot), <B for char val (1 byte: for on/off button)
        self._ble.gatts_write(self._handle, struct.pack("<hB", int(adcVal), buttonVal))
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
        buttonState = button.value()
        # Write every second, notify every 10 seconds.
        i = (i + 1) % 10
        adc.set_adcVal(pot_value, buttonState, notify=i == 0)
        time.sleep_ms(50)
    

if __name__ == "__main__":
    demo()
