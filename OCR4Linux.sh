#!/bin/bash
# ========================================================================================================================
# Author: Mohamed Hussein Al-Adawy
# Version: 1.2.0
# Description:
#     OCR4Linux is a versatile text extraction tool for Linux systems that:
#     1. Takes screenshots of selected areas using:
#        - grimblast for Wayland sessions
#        - scrot for X11 sessions
#     2. Performs Optical Character Recognition (OCR) using tesseract by passing the screenshot to a Python script
#     3. Copies extracted text to clipboard using:
#        - wl-copy and cliphist for Wayland
#        - xclip for X11
#
# Features:
#     - Support for both Wayland and X11 sessions
#     - Configurable screenshot directory
#     - Optional logging functionality
#     - Optional screenshot retention
#     - Command-line interface with various options
#
# Dependencies:
#     - tesseract-ocr: For text extraction
#     - grimblast/scrot: For screenshot capture
#     - wl-clipboard/xclip: For clipboard operations
#     - Python 3.x: For image processing
#
# Usage:
#     ./OCR4Linux.sh [-r] [-d DIRECTORY] [-l] [-h]
#     See './OCR4Linux.sh -h' for more details
# ========================================================================================================================

SCREENSHOT_NAME="screenshot_$(date +%d%m%Y_%H%M%S).jpg"
SCREENSHOT_DIRECTORY="$HOME/Pictures/screenshots"
OCR4Linux_HOME="$HOME/.config/OCR4Linux"
OCR4Linux_PYTHON_NAME="OCR4Linux.py"
TEXT_OUTPUT_FILE_NAME="output_text.txt"
LOGS_FILE_NAME="OCR4Linux.log"
SLEEP_DURATION=0.5
REMOVE_SCREENSHOT=false
KEEP_LOGS=false

# Display help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo "Options:"
    echo "  -r            Remove screenshot in the screenshot directory"
    echo "  -d DIRECTORY  Set screenshot directory (default: $SCREENSHOT_DIRECTORY)"
    echo "  -l            Keep logs"
    echo "  -h            Show this help message, then exit"
    echo "Example:"
    echo "  OCR4Linux.sh -s -d $HOME/screenshots -l"
    echo "  OCR4Linux.sh -s -l"
    echo "  OCR4Linux.sh -h"
    echo "Note:"
    echo "  if you run \`OCR4Linux.sh\` only without any arguments, it will save the screenshot in the default directory $SCREENSHOT_DIRECTORY."
}

# Parse command line arguments
while getopts "rd:lh" opt; do
    case $opt in
    r) REMOVE_SCREENSHOT=true ;;
    d) SCREENSHOT_DIRECTORY="$OPTARG" ;;
    l) KEEP_LOGS=true ;;
    h)
        show_help
        exit 0
        ;;
    *)
        show_help
        exit 1
        ;;
    esac
done

# Add log function
log_message() {
    local message
    message="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$message" >&2
    if [ "$KEEP_LOGS" = true ]; then
        {
            echo "$message"
        } >>"$OCR4Linux_HOME/$LOGS_FILE_NAME"
    fi
}

# Check if the required files exist.
check_if_files_exist() {
    log_message "Checking required files and directories..."

    # Validate screenshot directory
    if [ ! -d "$SCREENSHOT_DIRECTORY" ]; then
        log_message "Creating screenshot directory: $SCREENSHOT_DIRECTORY since it does not exist."
        if ! mkdir -p "$SCREENSHOT_DIRECTORY"; then
            log_message "ERROR: Failed to create directory $SCREENSHOT_DIRECTORY"
            exit 1
        fi
        log_message "Successfully created screenshot directory: $SCREENSHOT_DIRECTORY"
    fi

    # Check if the directory is writable
    if [ ! -w "$SCREENSHOT_DIRECTORY" ]; then
        log_message "ERROR: $SCREENSHOT_DIRECTORY is not writable"
        exit 1
    fi

    # Check if the python script exists.
    if [ ! -f "$OCR4Linux_HOME/$OCR4Linux_PYTHON_NAME" ]; then
        log_message "ERROR: $OCR4Linux_PYTHON_NAME not found in $OCR4Linux_HOME"
        exit 1
    fi
}

# take shots using grimblast for wayland
takescreenshot_wayland() {
    sleep $SLEEP_DURATION
    grimblast --notify copysave area "$SCREENSHOT_DIRECTORY/$SCREENSHOT_NAME"
}

# take shots using scrot for x11
takescreenshot_x11() {
    sleep $SLEEP_DURATION
    scrot -s -Z 0 -o -F "$SCREENSHOT_DIRECTORY/$SCREENSHOT_NAME"
}

# Run the screenshot functions based on the session type.
takescreenshot() {
    if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
        takescreenshot_wayland
    else
        takescreenshot_x11
    fi
    log_message "Screenshot saved to $SCREENSHOT_DIRECTORY/$SCREENSHOT_NAME"
}

# Pass the screenshot to OCR tool to extract text from the image.
extract_text() {
    python "$OCR4Linux_HOME/$OCR4Linux_PYTHON_NAME" \
        "$SCREENSHOT_DIRECTORY/$SCREENSHOT_NAME" \
        "$OCR4Linux_HOME/$TEXT_OUTPUT_FILE_NAME"
    log_message "Text extraction completed successfully"
}

# Copy the extracted text to clipboard using wl-copy and cliphist.
copy_to_wayland_clipboard() {
    cliphist store <"$OCR4Linux_HOME/$TEXT_OUTPUT_FILE_NAME"
    cliphist list | head -n 1 | cliphist decode | wl-copy
}

# Copy the extracted text to clipboard using xclip.
copy_to_x11_clipboard() {
    xclip -selection clipboard -t text/plain -i "$OCR4Linux_HOME/$TEXT_OUTPUT_FILE_NAME"
}

# Run the copy to clipboard functions based on the session type.
run_copy_to_clipboard() {
    if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
        copy_to_wayland_clipboard
    else
        copy_to_x11_clipboard
    fi
    rm "$OCR4Linux_HOME/$TEXT_OUTPUT_FILE_NAME"
    log_message "The extracted text has been copied to the clipboard."
}

# Remove the screenshot if the -r option is passed.
remove_image() {
    if [ "$REMOVE_SCREENSHOT" = true ]; then
        rm "$SCREENSHOT_DIRECTORY/$SCREENSHOT_NAME"
        log_message "Screenshot $SCREENSHOT_NAME has been deleted since you passed the -l option."
    fi
}

# Run the functions
main() {
    check_if_files_exist
    takescreenshot
    extract_text
    run_copy_to_clipboard
    remove_image
    log_message "The script has finished successfully."
    log_message "====================================================================================================="
}

main
