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
#     - rofi: For language selection menu
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
LANG_SPECIFIED=false
SPECIFIED_LANGS=""

langs=()

# Display help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo "Options:"
    echo "  -r                Remove screenshot in the screenshot directory"
    echo "  -d DIRECTORY      Set screenshot directory (default: $SCREENSHOT_DIRECTORY)"
    echo "  -l                Keep logs"
    echo "  --lang LANGUAGES  Specify OCR languages (e.g., 'all', 'eng', 'eng+ara')"
    echo "  -h                Show this help message, then exit"
    echo "Example:"
    echo "  OCR4Linux.sh -d $HOME/screenshots -l"
    echo "  OCR4Linux.sh --lang eng+ara"
    echo "  OCR4Linux.sh --lang all -l"
    echo "  OCR4Linux.sh -h"
    echo "Note:"
    echo "  - If --lang is not specified, an interactive language selection menu will appear"
    echo "  - Use 'all' to select all available languages"
    echo "  - Use '+' to separate multiple languages (e.g., 'eng+ara+fra')"
    echo "  - Without arguments, screenshots are saved to $SCREENSHOT_DIRECTORY"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -r)
            REMOVE_SCREENSHOT=true
            shift
            ;;
        -d)
            SCREENSHOT_DIRECTORY="$2"
            shift 2
            ;;
        -l)
            KEEP_LOGS=true
            shift
            ;;
        --lang)
            SPECIFIED_LANGS="$2"
            LANG_SPECIFIED=true
            shift 2
            ;;
        -h)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
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

    # Check if rofi is installed
    if ! command -v rofi &> /dev/null; then
        log_message "ERROR: rofi is not installed. Please install rofi to use language selection."
        exit 1
    fi

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

# Process specified languages from command line
process_specified_langs() {
    log_message "Processing specified languages: $SPECIFIED_LANGS"
    
    # Handle "all" case
    if [[ "$SPECIFIED_LANGS" == "all" ]]; then
        mapfile -t langs < <(tesseract --list-langs | awk 'FNR>1')
        log_message "Using ALL available languages: $(IFS=+ ; echo "${langs[*]}")"
    else
        # Split the language string by '+' and populate the langs array
        IFS='+' read -ra langs <<< "$SPECIFIED_LANGS"
        log_message "Using specified languages: $(IFS=+ ; echo "${langs[*]}")"
        
        # Validate that the specified languages are available
        available_langs=$(tesseract --list-langs | awk 'FNR>1')
        for lang in "${langs[@]}"; do
            if ! echo "$available_langs" | grep -q "^$lang$"; then
                log_message "WARNING: Language '$lang' is not available on this system"
            fi
        done
    fi
}

# Choose languages for OCR using rofi
choose_lang() {
    log_message "Fetching available languages for OCR selection..."
    
    # Get available languages and add "ALL" option at the beginning
    mapfile -t langs < <(tesseract --list-langs | awk 'BEGIN {print "ALL" } FNR>1' | rofi -dmenu -multi-select -p "Select OCR Languages:")

    if [ ${#langs[@]} -eq 0 ]; then
        log_message "CANCELLED: User aborted language selection"
        exit 1
    fi

    # If "ALL" is selected, use all available languages
    if [[ " ${langs[*]} " =~ " ALL " ]]; then
        mapfile -t langs < <(tesseract --list-langs | awk 'FNR>1')
        log_message "Selected ALL languages: $(IFS=+ ; echo "${langs[*]}")"
    else
        log_message "Selected languages: $(IFS=+ ; echo "${langs[*]}")"
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
    # Create language string for passing to Python script
    local lang_string=""
    if [ ${#langs[@]} -gt 0 ]; then
        lang_string=$(IFS=+; echo "${langs[*]}")
    fi
    
    if [ -n "$lang_string" ]; then
        python "$OCR4Linux_HOME/$OCR4Linux_PYTHON_NAME" \
            "$SCREENSHOT_DIRECTORY/$SCREENSHOT_NAME" \
            "$OCR4Linux_HOME/$TEXT_OUTPUT_FILE_NAME" \
            --langs "$lang_string"
    else
        python "$OCR4Linux_HOME/$OCR4Linux_PYTHON_NAME" \
            "$SCREENSHOT_DIRECTORY/$SCREENSHOT_NAME" \
            "$OCR4Linux_HOME/$TEXT_OUTPUT_FILE_NAME"
    fi
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
    
    # Handle language selection
    if [ "$LANG_SPECIFIED" = true ]; then
        process_specified_langs
    else
        choose_lang
    fi
    
    takescreenshot
    extract_text
    run_copy_to_clipboard
    remove_image
    log_message "The script has finished successfully."
    log_message "====================================================================================================="
}

main
