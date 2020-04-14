## ESP32 acts as Bluetooth Low Energy peripheral device, broadcasts sensor data

We are using micropython here on the ESP32. All information for firmware preparations are available at the [official ESP32 micropython introduction tutorial](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)

I am using [Thonny](https://thonny.org/) on Linux to connect and load all included files to the device.

Explanation of each file included:<br />

- boot.py
    - First file to run when ESP32 is turned on. While developing I decided to open a command access via local internet connection using [webrepl](https://docs.micropython.org/en/latest/esp8266/tutorial/repl.html). For this reason it is necessary to edit this file to be compatible with your own internet router (i.e. change SSID and password). Included in this file is equally preparation for use of an oled screen to display the device's ip adddress. Further information follows below. <br />

- webrepl_cfg.py
    - Must be edited to include a password of your choice, if you wish to access the webrepl that is.

- ssd1306.py
    - The ESP32 used for this project is a [Heltec Wifi Kit 32](https://heltec.org/project/wifi-kit-32/). This model has an oled screen included. This file is required for support.

- ble_advertising
    - Helper for generating BLE advertising payloads. Lifted from the bluetooth section of the github [micropython repository](https://github.com/micropython/micropython/tree/master/examples/bluetooth)

- main.py
    - The code found here was originally the ble_temperature.py code found in the github [micropython repository](https://github.com/micropython/micropython/tree/master/examples/bluetooth). I modified this code, replacing the temperature values with those of a potentiometer connected to pin 32. These values will be advertised to the world when this code is executed.

