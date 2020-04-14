import webrepl #library for accessing ESP device from a browser
import network
import ssd1306 #library for oled screen
import machine # library for I/O pins
import time

# Activation OLED
i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))
reset_oled = machine.Pin(16, machine.Pin.OUT)
reset_oled.value(0)
time.sleep(.05)
reset_oled.value(1)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # 128 x 64 pixels

#network setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
oled.fill(0)  # erase screen
oled.text("connecting", 22, 20)
oled.text("to network", 22, 35)
oled.show()

#time.sleep(10) #buffer
wlan.connect('SSID', 'PASSWORD') # replace for your router
time.sleep(10) # Wait for DHCP stuff to finish up
ip_result = list(wlan.ifconfig())
#show ip address on screen
oled.fill(0)  # efface l’ecran
oled.text("My address is", 1, 20)
oled.text(ip_result[0],1, 40)
oled.show()

webrepl.start()





