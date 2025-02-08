6 Oct 2024
Silvan Roth

# Foggy

<img src="/images/FinalWide.jpeg" width="100%"/>


Foggy_ is a project that explores the rendering of an impressionistic visual of another place or scene through primitive technology. 

The idea was to create a "portal to another place via a pixelated camera stream", not meant to provide the user with accurate data but simply conveying a vague impression of the other place. If there are people moving on the other side, the idea was to let the user feel this presence, possibly even alleviating feelings of loneliness (even if subconscious).

## Implementation
I used the following process to display videos on the 8x8 LED Matrix:

<img src="/images/software.png" width="100%"/>

### Software

- FFMPEG Shell script: This script cropped the selected videos to a square format, scaled them down to 8x8 pixels, and extracted pngs of the frames at a defined FPS, saved in a folder called "frames".
- Python script: To output videos on the LED matrix, a python script iterates through all the frames in the folder and displays them on the neopixel grid sequentially, making it appear animated.

### Hardware

<img src="/images/wiringfull.png" width="100%"/>


The hardware currently consists of an 8x8 WS2811 LED Matrix connected to a Raspberry Pi 3 via the GPIO 18 and GND pins, both powered by a 5V USB-C power delivery board. The LEDs and Raspberry Pi can respectively consume up to 1.2A at peak load, so the entire setup requires 
 and using a level shifter breakout board to convert the Raspberry Pi's 3.3V logic to the 5V logic required by the Neopixels. I developed on the Raspberry Pi in a headless setup using VNC viewer, connected via ethernet. The enclosure is 3D printed PLA. The diffusion lenses are sand blasted laser cut acrylic rectangles.

<img src="/images/hardwareprototyping.png" width="100%"/>



<img src="/images/diffuserlevels.png" width="100%"/>

<img src="/images/enclosure.png" width="100%"/>

### Final presentation

To present hardware effectively, a systemd service file can automatically play the LED animation on startup:

```
sudo nano /etc/systemd/system/ledcontrol.service
```
```
[Unit]
Description=LED Control Script
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/pi/NeopixelAnimateAll.py # <-- The script to execute
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
```
Enable the ledcontrol.service and reboot to verify that it works
```
sudo systemctl enable ledcontrol.service
sudo systemctl start ledcontrol.service
sudo reboot
```


<img src="/images/FinalInsert.jpeg" width="49.65%"/> <img src="/images/FinalFull.png" width="49%"/>





## Limitations and improvements

The current version is limited in a few ways that, in a next version, could be improved as follows:
- Memory of the Raspberry Pi - Use a newer Raspberry Pi or optimize code to pre-load all the image data more efficiently. Consider converting to BMP instead of PNG for more efficient rendering.
- Color accuracy and contrast - implement gamma correction and color correction filters.
- Occasional glitching - Possibly due to fluctuations in current, LED matrix acts erratically sometimes. Other potential causes might be poor connections (I have been using dupont connectors), the quality of the LED matrix, signal noise caused by the level shifter. Using a high quality power brick and cable helps.
