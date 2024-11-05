#!/bin/bash

FPS=10

#output resolutions
RESOLUTIONS=("8x8")

# Directory containing the original videos
ORIGINAL_DIR="Original"


# Check if the original directory exists

echo "Finding source material"
if [ ! -d "$ORIGINAL_DIR" ]; then
  echo "Error: Directory '$ORIGINAL_DIR' does not exist."
  exit 1
fi

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

    # Extract frames as images (optional)
    mkdir -p "${OUTPUT_DIR}/frames"
    ffmpeg -i "${OUTPUT_DIR}/video_${WIDTH}x${HEIGHT}.mp4" -vf fps=${FPS} "${OUTPUT_DIR}/frames/frame_%04d.png"

    echo "Conversion of $INPUT_VIDEO to ${WIDTH}x${HEIGHT} completed."
  done
done

echo "All videos processed."
