#!/usr/bin/env python
import sys, errno
from gpiozero import PWMLED
import binascii
import struct
import time
import OSC
import os
import bluepy.btle
from bluepy.btle import UUID, Peripheral, BTLEDisconnectError, BTLEInternalError

led = PWMLED(13)

ESP_MAC_ADDR = "a4:cf:12:02:c3:6e"
adc_uuid = UUID(0x2A58)
p = Peripheral()

#-------------- init puredata stuff ------------------
os.system('puredata -nogui -audiodev 3 recv-adc.pd &')
print "=============="
print "starting PD!!!"
print "=============="
time.sleep(1)
send_address = '127.0.0.1', 8001
c = OSC.OSCClient()
c.connect(send_address)   # localhost, port 8001
oscmsg = OSC.OSCMessage()
oscmsg.setAddress("/pdRecv") #address name is declared in pd patch


def sendMsg(val):
    oscmsg.append(val)
    c.send(oscmsg)
    oscmsg.remove(val)

while 1:
    try:
        print "attempting to connect to ", ESP_MAC_ADDR
        p.connect(ESP_MAC_ADDR, "public") #replace with mac address of the ESP32
        print "SUCCESS"
        ch = p.getCharacteristics(uuid=adc_uuid)[0]

        if (ch.supportsRead()):
            while 1:
                val = binascii.b2a_hex(ch.read())
                val = binascii.unhexlify(val)
                val = struct.unpack('<h', val)[0]
                print str(val)
                sendMsg(val)
                ledVal = val / 4095.0 # we are receiving 0 to 4095 (12-bits)
                led.value = ledVal

    except IOError as e:
        if e.errno == errno.EPIPE:
            print "IO error... ignoring"
            time.sleep(.5)
            p = Peripheral() # re-initialize peripheral
            p.disconnect()
            continue

    except BTLEDisconnectError:
        print "Device disconnected!"
        time.sleep(.5)
        print "connect is false"
        p.disconnect()
        continue

    except BTLEInternalError:
        print "internal error... ignoring"
        time.sleep(.5)
        p.disconnect()
        continue
