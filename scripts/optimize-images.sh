#!/bin/bash
set -euo pipefail

# Image optimization script
# Originals live in /Users/nijkampr/stuff/itsrene.dj-originals (see docs/adr/0003)
# Run this script after adding new originals there to regenerate web derivatives.

ORIG_DIR="/Users/nijkampr/stuff/itsrene.dj-originals"

# Define optimization jobs: SOURCE_FILE DEST_PATH TARGET_WIDTH QUALITY
# Adjusted quality: headshot at 50, bb_summerparty at 60 to stay under 250KB
declare -a JOBS=(
    "headshot.jpg images/headshot.jpg 900 50"
    "actionshots/53799606763_6e1930e6e3_o.jpg images/actionshots/53799606763_6e1930e6e3_o.jpg 1200 72"
    "actionshots/53799606928_2f35cccc61_o.jpg images/actionshots/53799606928_2f35cccc61_o.jpg 1200 72"
    "actionshots/bb_summerparty.jpg images/actionshots/bb_summerparty.jpg 1200 60"
    "actionshots/FB_IMG_1697890143498.jpg images/actionshots/FB_IMG_1697890143498.jpg 1080 72"
)

# Ensure output directories exist
mkdir -p images/actionshots

# Process each job
declare -a RESULTS
any_oversized=0

for job in "${JOBS[@]}"; do
    read -r src dest width quality <<< "$job"
    src_path="$ORIG_DIR/$src"

    if [ ! -f "$src_path" ]; then
        echo "ERROR: Source not found: $src_path" >&2
        exit 1
    fi

    # Optimize: resize to max width and set JPEG quality
    sips --resampleWidth "$width" -s format jpeg -s formatOptions "$quality" "$src_path" --out "$dest" > /dev/null 2>&1

    # Get output dimensions and size
    dims=$(sips -g pixelWidth -g pixelHeight "$dest" 2>/dev/null | grep -E "pixelWidth|pixelHeight" | awk '{print $2}' | tr '\n' 'x' | sed 's/x$//')
    size=$(stat -f%z "$dest")

    RESULTS+=("$dest|$dims|$size")

    if [ "$size" -gt 250000 ]; then
        any_oversized=1
    fi
done

# Print table
echo ""
echo "OUTPUT PATH | DIMENSIONS | BYTES"
echo "------------|------------|----------"
for result in "${RESULTS[@]}"; do
    IFS='|' read -r path dims size <<< "$result"
    printf "%-35s | %-12s | %8d\n" "$path" "$dims" "$size"
done
echo ""

# Check for oversized files
if [ $any_oversized -eq 1 ]; then
    echo "ERROR: One or more outputs exceed 250000 bytes" >&2
    for result in "${RESULTS[@]}"; do
        IFS='|' read -r path dims size <<< "$result"
        if [ "$size" -gt 250000 ]; then
            echo "  - $path ($size bytes)" >&2
        fi
    done
    exit 1
fi

echo "✓ All images optimized successfully"
