# Seaborn_Micro
Micro Python libraries for controlling LED lights

## Files
    seaborn_esp -- contains wrapper code to setup networks and get real time
                   clock RTC.
    seaborn_neopixel -- contains wrapper code around neopixels.

    micro_secrets -- this contains passwords and will not be in the repo
                     ESSID is the network name
                     ESSID_PWD is the password for the network
                     NAME is the custom name for the microchip
                     INDEX is the custom index for the microship

    # the rest are scripts for various projects
    bullet_hole


## Setup Micro Python Commands

ls /dev/cu.*

esptool.py --p /dev/cu.SLAB_USBtoUART    -c esp8266 -b 921600 erase_flash
esptool.py --p /dev/cu.SLAB_USBtoUART    -c esp8266 -b 921600 write_flash --flash_size=detect 0 ../esp8266-20191220-v1.12.bin 
ampy --port /dev/cu.SLAB_USBtoUART put seaborn_neopixel.py seaborn_neopixel.py


### modify micro_secrets first
ampy --port /dev/cu.SLAB_USBtoUART put micro_secrets.py micro_secrets.py
ampy --port /dev/cu.SLAB_USBtoUART put seaborn_neopixel.py seaborn_neopixel.py
ampy --port /dev/cu.SLAB_USBtoUART put seaborn_esp.py seaborn_esp.py

ampy --port /dev/cu.SLAB_USBtoUART put <main>.py main.py



Screen /dev/cu.SLAB_USBtoUART 115200


## Simple HTTP Server
http://docs.micropython.org/en/v1.8.7/esp8266/esp8266/tutorial/network_tcp.html#simple-http-server


## WEB REPL
http://docs.micropython.org/en/latest/esp8266/quickref.html#webrepl-web-browser-interactive-prompt

starting webrepl


## RTC (Real Time Clock)
https://www.amazon.com/gp/product/B01IXXACD0/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01IXXACD0&linkCode=as2&tag=shophow2elect-20&linkId=bc118e74bb1117288bd944167332a787
Buy a module to keep the real clock setting, but I see if request_rtc works.


# WLED

esptool.py --p /dev/cu.SLAB_USBtoUART    -c esp8266 -b 921600 erase_flash
esptool.py --p /dev/cu.SLAB_USBtoUART    -c esp8266 -b 921600 write_flash --flash_size=detect 0 ./wled/WLED_0.11.0_ESP8266.bin

https://github.com/Aircoookie/WLED/releases

pwd: wled1234

