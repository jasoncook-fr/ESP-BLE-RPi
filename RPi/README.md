## Python code for connecting and receiving data from ESP32 peripheral bluetooth device
The code here is to be run only after you have setup the ESP32. You will need to change the parameters in the code found here, specifically entering the MAC address of the ESP32. To discover the MAC address of the ESP32 you can run the following command from the Raspberry Pi 3:
```
sudo blescan
```

Python bluepy module is required for this code. On Raspbian or other Debian-based system:
```
$ sudo apt-get install python-pip libglib2.0-dev
$ sudo pip install bluepy
```
If that doesn't work out, then do it from the source
```
$ sudo apt-get install git build-essential libglib2.0-dev
$ git clone https://github.com/IanHarvey/bluepy.git
$ cd bluepy
$ python setup.py build
$ sudo python setup.py install
```

## License
This project uses code from the bluez project, which is available under the Version 2 of the GNU Public License.

The Python files are released into the public domain by their author, Ian Harvey. 

The rest is included by Jason Cook

