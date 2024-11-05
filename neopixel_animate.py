# LIBRARIES****************************************************************

from PIL import Image
import board
import neopixel
import os
import glob
import time

# NeoPixel Configuration***************************************************
MATRIX_WIDTH = 8
MATRIX_HEIGHT = 8
PIXEL_PIN = board.D18
NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT
ORDER = neopixel.GRB

FRAMES_FOLDER = "frames_city"
FRAME_DELAY = 0.1

pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    brightness=0.08,
    auto_write=False,
    pixel_order=ORDER
)

# Image File Configuration*************************************************

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the frames folder
frames_path = os.path.join(script_dir, FRAMES_FOLDER)

# Optional: Check if the image file exists
#if not os.path.isfile(frames_path):
#    print(f"Error: Image file not found at {image_path}")
#    exit(1)

# FUNCTIONS****************************************************************

# Convert the xy coordinates to an index
def xy_to_index(x, y, width, height):
    index = (height-1-y)*width+(width-1-x)
    return index
 
# MAIN PROGRAM*************************************************************
   
try:   
   # Get a list of all image files in the frames folder
    image_files = sorted(
        glob.glob(os.path.join(frames_path, '*')),
        key=lambda x: os.path.basename(x)
    )

    # Check if any image files were found
    if not image_files:
        print("No image files found in {}".format(frames_path))
        exit(1)
        
    # Create array of images
    imageList = []
    for image_path in image_files:
        # Load the image
        imageList.append(Image.open(image_path).convert('RGB'))


    while True:

        for image in imageList:
            # Optional: Resize the image if it's not 8x8
#            if image.size != (MATRIX_WIDTH, MATRIX_HEIGHT):
 #               image = image.resize((MATRIX_WIDTH, MATRIX_HEIGHT))
            """
            pixel_data = image.load()

            # Set NeoPixel colors based on image pixels
            for y in range(MATRIX_HEIGHT):
                for x in range(MATRIX_WIDTH):
                    r, g, b = pixel_data[x, y]
                    index = xy_to_index(x, y, MATRIX_WIDTH)
                    pixels[index] = (g, r, b)  # Adjust for GRB color order
            """


            # Set NeoPixel colors based on image pixels
            for y in range(MATRIX_HEIGHT):
                for x in range(MATRIX_WIDTH):
                    r, g, b = image.getpixel((x,y))
                    index = xy_to_index(x, y, MATRIX_WIDTH, MATRIX_HEIGHT)
                    pixels[index] = (r, g, b)  # Adjust for GRB color order

            # Update the NeoPixel matrix
            pixels.show()

            # Control the animation speed
            time.sleep(FRAME_DELAY)  # Adjust delay as needed
except KeyboardInterrupt:
    print("Animation stopped by user.")
    pixels.fill((0, 0, 0))
    pixels.show()
