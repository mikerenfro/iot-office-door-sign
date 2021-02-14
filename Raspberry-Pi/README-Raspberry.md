# An Internet of Things Office Door Sign using a Raspberry Pi and an LCD

![Door sign]

## Motivation

See [the original README](https://github.com/mikerenfro/iot-office-door-sign), except by mid-2019, I decided a Pi and and LCD were worth the additional cost over a PyPortal.
This accomplishes the same goals as the PyPortal version, I've just replaced the PyPortal with a Raspberry Pi with auto-login and Chromium pointing to a jQuery web page.

## Prerequisites

See [the original README](https://github.com/mikerenfro/iot-office-door-sign), except by replacing the PyPortal with a Raspbery Pi and an LCD.
My implementation uses a Raspberry Pi Zero W, a [HyperPixel 4](https://www.adafruit.com/product/3932) LCD, Raspbian, and LXDE.

## Web Front End

See [the original README](https://github.com/mikerenfro/iot-office-door-sign).
No changes required.

## Server Back End

See [the original README](https://github.com/mikerenfro/iot-office-door-sign).
No changes required to the parts where I convert the latest tweet into JSON.
I am now hosting a small jQuery web page on the same server, but the page could be stored at any valid URL.
You'll also need a copy of jquery-backstretch.min.js from [the Backstretch project](https://github.com/jquery-backstretch/jquery-backstretch).

See rpi-door.html in this folder for some sample page contents.
Edit graphic URLs, JSON URLs, fonts, and other visual settings as appropriate.

## Raspberry Pi

Enable auto-login on the Pi.
I'm using LXDE on the Pi, so I made a file `~pi/.config/lxsession/LXDE-pi/autostart` containing:

    xset s off
    xset -dpms
    xset s noblank
    @chromium-browser --kiosk --app=https://PAGE_URL

where `PAGE_URL` is the location of the web page detailed above.

When completed and running, the default settings with a small Ganglia graph look like the photo below.

![Door sign]

[Door sign]: door-sign.jpg
