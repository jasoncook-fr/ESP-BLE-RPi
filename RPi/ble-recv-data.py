#!/usr/bin/env python

import binascii
import struct
import time
from bluepy.btle import UUID, Peripheral, BTLEDisconnectError, BTLEInternalError

adc_uuid = UUID(0x2A6E)
p = Peripheral()
p.connect("bt:ma:ca:dd:re:ss", "public") #replace with mac address of the ESP32

def main():
    print("connecting...")
    ch = p.getCharacteristics(uuid=adc_uuid)[0]
    if (ch.supportsRead()):
        while 1:
            try:
                val = binascii.b2a_hex(ch.read())
                val = binascii.unhexlify(val)
                val = struct.unpack('<h', val)[0]
                print str(val)
                time.sleep(.01)

            except BTLEDisconnectError:
                print "Device disconnected!"
                continue

            except BTLEInternalError:
                print "internal error... ignoring"
                time.sleep(.5)
                print "attempting to reconnect..."
                p.connect("bt:ma:ca:dd:re:ss", "public") #replace with mac address of the ESP32
                ch = p.getCharacteristics(uuid=adc_uuid)[0]
                if (ch.supportsRead()):
                    continue
                else:
                    "no connection!!!"

if __name__ == '__main__':
        main()
