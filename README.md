6 Oct 2024
Silvan Roth


## Aim
_Foggy_ is a project that explores the rendering of an impressionistic visual of another place through very primitive technology. 

The idea was to create a "portal to another place via a pixelated camera stream", not meant to provide the user with accurate data but simply conveying a vague impression of the other place. If there are people moving on the other side, the idea was to let the user feel this presence, possibly even alleviating feelings of loneliness (even if subconscious).

## Implementation
I used the following process to display videos on the 8x8 LED Matrix:

<img src="/images/software.png" width="60%"/>

### Software

- FFMPEG Shell script: This script cropped the selected videos to a square format, scaled them down to 8x8 pixels, and extracted pngs of the frames at a defined FPS, saved in a folder called "frames".
- Python script: To output videos on the LED matrix, a python script iterates through all the frames in the folder and displays them on the neopixel grid sequentially, making it appear animated.

### Hardware

<img src="/images/hardwareblocks.png" width="60%"/>

The hardware currently consists of a 8x8 WS2811 LED Matrix connected to a Raspberry Pi 3 via the GPIO 18 and GND pins, powered by 5V from a USB-C power delivery board (allowing it to draw as much current as it might need) and using a level shifter breakout board to convert the Raspberry Pi's 3.3V logic to the 5V logic required by the Neopixels. I developed on the Raspberry Pi in a headless setup using VNC viewer, connected via ethernet. The enclosure is 3D printed PLA. The diffusion lenses are sand blasted laser cut acrylic rectangles.

<img src="/images/hardwareprototyping.png" width="60%"/>

<img src="/images/enclosure" width="60%"/>

<img src="/images/diffuserlevels.png" width="60%"/>

## Limitations and improvements

<img src="/images/final.png" width="60%"/>

The current version is limited in a few ways that, in a next version, could be improved as follows:
- Memory of the Raspberry Pi - Use a newer Raspberry Pi or optimize code to pre-load all the image data more efficiently.
- Speed of the LED panel - Maybe the WS2811 LEDs that I have used are not the ideal choice.
- Color accuracy and contrast - implement gamma correction and color correction filters.
- Frequent glitching - I do not currently know the exact source of this, but half of the display occasionally malfunctions/acts erratically. A potential cause might be poor connections (I have been using dupont connectors), the quality of the LED matrix, signal noise caused by the level shifter, or 
- Running the script manually in VNC viewer (virtual desktop), which required exact file paths, multiple command line commands, and caused frustration/cost time as the viewer crashed or could not connect to the pi - Improve by writing a script to auto-run the python program on startup, no virtual desktop viewer needed.
