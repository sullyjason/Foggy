6 Oct 2024
Silvan Roth


## Introduction

The aim of Studio 1 was to explore the concept of "Photolipsia", defined as the capturing and representation of reality through visual means. We were to embark on our own independent exploration, with a presentation at the end and some form of product to illustrate our findings. 

### Idea
Over the course of the first few theory inputs I often contemplated the concept of "Resolution". I thought it was interesting that we are converging on this near-perfect resolution representation of both 2D and 3D objects but wanted to question to what extent this is needed. I wanted to investigate whether very low-resolution visuals could have similarly powerful subconscious effects as higher resolution visuals, thus exploring whether the visual resolution was really a relevant factor in convincing us that something is "real".

The idea was to create a "portal to another place via a pixelated camera" (see sketch below), not meant to provide the user with accurate data but simply conveying a vague impression of the other place. If there are people moving on the other side, the idea was to let the user feel this presence, possibly even alleviating feelings of loneliness (even if subconscious).

## Process
Due to the limited amount of time I intended to use supplies I already had for prototyping. 
1.  My first and original idea involved using an ESP32CAM (ESP32 microcontroller with built in camera and SD card slot) to stream live footage to another ESP32 controlling a 64x64 LED Matrix via the HUB75 interface. 
2. I quickly realized that it might be easier to demonstrate using a Raspberry Pi due to its memory and processing capabilities, as I was intending to control quite a large amount of LEDs. 
3. After a mentoring session I realized that demo videos would likely be far more effective at conveying my message, letting me choose what scene I want to show and being much simpler to implement technically. I also decided to switch to an existing 8x8 LED Matrix that I already had, as its form factor made it easy to transport and I didn't need to build my own grid from one long string of LEDs.

![[DesignProcess.png]]


## Final Implementation
I used the following process to display videos on the 8x8 LED Matrix:

![[Pasted image 20241004193944.png]]

### Videos
As my initial idea was to create a blurry window to another place, I started by taking videos from real life. This process turned out to be surprisingly meditative - I walked around Irchel park, Toni Areal and the Hardbrücke area looking for scenes or elements that you would expect to see through a window. Ideally they had to contain high contrast and some organic movement, as my theory was that this movement would be what makes it recognizable later.
![[Pasted image 20241006205403.png]]
Later I added iconic scenes such as scenes from Disney movies and music videos to the collection.
![[Pasted image 20241006205618.png]]

### FFMPEG Shell script
This script cropped the selected videos to a square format, scaled them down to 8x8 pixels, and extracted pngs of the frames at a defined FPS, saved in a folder called "frames".

```sh
#!/bin/bash

FPS=10

#output resolutions
RESOLUTIONS=("8x8")

# Directory containing the original videos
ORIGINAL_DIR="Original"

# Check if there are any mp4 files in the original directory
MP4_FILES=("$ORIGINAL_DIR"/*.MOV)

if [ "${#MP4_FILES[@]}" -eq 0 ]; then
  echo "Error: No .mp4 files found in '$ORIGINAL_DIR'."
  exit 1
fi

#loop over input video
for INPUT_VIDEO in "$ORIGINAL_DIR"/*.MOV; do

echo "processing $INPUT_VIDEO"

  # Get the base name of the video file (without directory and extension)
  VIDEO_BASENAME=$(basename "$INPUT_VIDEO" .mp4)

  # Loop over each resolution
  for RES in "${RESOLUTIONS[@]}"; do
    WIDTH=$(echo $RES | cut -dx -f1)
    HEIGHT=$(echo $RES | cut -dx -f2)

    # Create output directory for this video and resolution
    OUTPUT_DIR="${VIDEO_BASENAME}_${WIDTH}x${HEIGHT}"
    mkdir -p "$OUTPUT_DIR"

    # Convert video to the specified resolution and frame rate
    ffmpeg -i "$INPUT_VIDEO" -vf "crop='min(iw,ih)':'min(iw,ih)':'((iw - min(iw,ih))/2)':'((ih - min(iw,ih))/2)',scale=${WIDTH}:${HEIGHT},fps=${FPS}" -c:v libx264 -pix_fmt yuv420p "${OUTPUT_DIR}/video_${WIDTH}x${HEIGHT}.mp4"

    # Extract frames as images
    mkdir -p "${OUTPUT_DIR}/frames"
    ffmpeg -i "${OUTPUT_DIR}/video_${WIDTH}x${HEIGHT}.mp4" -vf fps=${FPS} "${OUTPUT_DIR}/frames/frame_%04d.png"

    echo "Conversion of $INPUT_VIDEO to ${WIDTH}x${HEIGHT} completed."
  done
done

echo "All videos processed."
```

### Python script
To output videos on the LED matrix, a python script iterates through all the frames in the folder and displays them on the neopixel grid sequentially, making it appear animated.

```python
#!/usr/bin/env python3

# LIBRARIES****************************************************************
from PIL import Image
import board
import neopixel
import os
import glob
import time
import re  # natural sorting

# NeoPixel Configuration**************************************************
MATRIX_WIDTH = 8
MATRIX_HEIGHT = 8
PIXEL_PIN = board.D18
NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT
ORDER = neopixel.GRB

FRAMES_FOLDERS = ['frames_2', 'frames_3', 'frames_4']  # List of folders
FRAME_DELAY = 0.1  # time between frames

pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    brightness=0.08,
    auto_write=False,
    pixel_order=ORDER
)

# FUNCTIONS****************************************************************

# sorting the images numerically
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

# function to rotate image 
def xy_to_index(x, y, width, height):
    index = (height - 1 - y) * width + (width - 1 - x)
    return index

# MAIN PROGRAM*************************************************************

try:
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        for folder in FRAMES_FOLDERS:
            frames_path = os.path.join(script_dir, folder)
            # Get a list of all image files in the current frames folder
            image_files = sorted(
                glob.glob(os.path.join(frames_path, '*')),
                key=natural_sort_key
            )

            # Check if any image files were found
            if not image_files:
                print("No image files found in {}".format(frames_path))
                continue  # Skip to next folder

            for image_path in image_files:
                # Load the image with error handling
                try:
                    image = Image.open(image_path).convert('RGB')
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
                    continue  # Skip to the next image
                    
                # Set NeoPixel colors based on image pixels
                for y in range(MATRIX_HEIGHT):
                    for x in range(MATRIX_WIDTH):
                        r, g, b = image.getpixel((x, y))
                        index = xy_to_index(x, y, MATRIX_WIDTH, MATRIX_HEIGHT)
                        pixels[index] = (g, r, b)  # Adjust for GRB color order

                # Update the NeoPixel matrix
                pixels.show()

                # Control the animation speed
                time.sleep(FRAME_DELAY)

                # Close the image to free memory
                image.close()

except KeyboardInterrupt:
    print("Animation stopped by user.")
    pixels.fill((0, 0, 0))
    pixels.show()
```

### Hardware

![[Pasted image 20241006195134.png]]
The hardware currently consists of a 8x8 WS2811 LED Matrix connected to a Raspberry Pi 3 via the GPIO 18 and GND pins, powered by 5V from a USB-C power delivery board (allowing it to draw as much current as it might need) and using a level shifter breakout board to convert the Raspberry Pi's 3.3V logic to the 5V logic required by the Neopixels. I developed on the Raspberry Pi in a headless setup using VNC viewer, connected via ethernet.

![[hardwareprototyping.png]]

### Light diffusers
Once the electronic setup worked and I was ready to develop the light diffusers, I found that this was the most fun part of the process so far - changing the brightness of the LEDs, the distance of a diffuser to the LED panel, the amount of sequential diffusers, and the amount that they were diffusing light all influenced how foggy the image looked. I decided to turn this into a feature of the final result - a slide system that let you change the amount of diffusion by removing or adding diffusion slides to the enclosure holding the Raspberry Pi and LED Matrix. 

![[diffuserlevels.png]]
### Enclosure
For this I 3D printed an enclosure, consisting of a base and a lid, connected with M2 screws and threaded inserts. An opening at the top of the LED matrix allows the user to switch out diffuser slides. The enclosure unintentionally ended up looking retro and cute, almost looking like a cartoon snail. I liked this aesthetic, as it felt inviting and matched the playful element of the light diffuser interaction.

![[Pasted image 20241006192520.png]]

### Final product
The final product looks as follows. I powered both the Raspberry Pi and the LED matrix with the same power supply and executed the python scripts using command line via the VNC virtual desktop. Once the python script was animating the LEDs, I had four slides with different levels of diffusion that I moved around to show the change in appearance. I played an animation of a public space (example used previously), the *Titanic* bow scene, and short segment of "The Circle of Life" from *The Lion King*.

![[Pasted image 20241006192819.png]]

## Reflection
This project, while short, was a rewarding experience where I felt I had a lot of freedom to try out new tools and attempt conceptual explorations. I thoroughly enjoyed the process with all the components involved, and appreciated the constant encouragement to explore the conceptual aspects.

### Limitations and improvements
The current version is limited in a few ways that, in a next version, could be improved as follows:
- Memory of the Raspberry Pi - Use a newer Raspberry Pi or optimize code to pre-load all the image data more efficiently.
- Speed of the LED panel - Maybe the WS2811 LEDs that I have used are not the ideal choice.
- Color accuracy and contrast - implement gamma correction and color correction filters.
- Frequent glitching - I do not currently know the exact source of this, but half of the display occasionally malfunctions/acts erratically. A potential cause might be poor connections (I have been using dupont connectors), the quality of the LED matrix, signal noise caused by the level shifter, or 
- Running the script manually in VNC viewer (virtual desktop), which required exact file paths, multiple command line commands, and caused frustration/cost time as the viewer crashed or could not connect to the pi - Improve by writing a script to auto-run the python program on startup, no virtual desktop viewer needed.

### Concept
As I explored this idea of creating blurry impressionistic abstractions of reality instead of sharp, high-definitions renderings, some things occured to me: 
- I expected the resulting image to be frustrating due to its lack of detail. However, to me the foggy representation felt surprisingly calm and comforting, the ghost-like figures feeling familiar. This might be because blurring the subjects makes them more anonymous and distant, which is maybe why they feel safe.
- We could argue that this is actually a more accurate representation of how we see the world. Our eyes can only ever focus on one specific point, while our peripheral vision is likely mostly a reconstruction ([article](https://www.sciencedaily.com/releases/2016/12/161208143425.htm))
- Imagination: personally, I enjoyed the way the resulting images triggered my imagination - by brain immediately started scanning for scenes that the image reminded me of, in many cases successfully, despite the low resolution.

