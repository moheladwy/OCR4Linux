#!/bin/bash
# ========================================================================================================================
# Author:
#     Mohamed Hussein Al-Adawy
# Description:
#     This script takes a screenshot of a selected area, extracts the text from the image, and copies it to the clipboard.
#     The script uses grimblast for Wayland and scrot for X11 to take screenshots.
#     The script uses tesseract to extract text from the image.
#     The script uses wl-copy and cliphist for Wayland and xclip for X11 to copy the extracted text to the clipboard.
#     The script uses a python script to extract text from the image.
#     The script requires the following packages to be installed:
#         - python
#         - tesseract
#         - grimblast or scrot
#         - wl-clipboard or xclip
#         - cliphist
# ========================================================================================================================

screenshot_name="screenshot_$(date +%d%m%Y_%H%M%S).jpg"
screenshot_dir="$HOME/Pictures/screenshots"
python_script_path="$HOME/.config/OCR4Linux"
python_script_name="OCR4Linux.py"
output_file_name="output_text.txt"
waiting_time=0.5

# Check if the required files exist.
check_if_files_exist() {
    # Check if the screenshot directory exists, if not create it.
    if [ ! -d "$screenshot_dir" ]; then
        mkdir -p "$screenshot_dir"
    fi

    # Check if the python script exists.
    if [ ! -f "$python_script_path/$python_script_name" ]; then
        echo "Error: $python_script_name not found in $python_script_path"
        exit 1
    fi
}

# take shots using grimblast for wayland
takescreenshot_wayland() {
    sleep $waiting_time
    grimblast --notify copysave area "$screenshot_dir/$screenshot_name"
}

# take shots using scrot for x11
takescreenshot_x11() {
    sleep $waiting_time
    scrot -s -Z 0 -o -F "$screenshot_dir/$screenshot_name"
}

# Run the screenshot functions based on the session type.
takescreenshot() {
    if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
        takescreenshot_wayland
    else
        takescreenshot_x11
    fi
}

# Pass the screenshot to OCR tool to extract text from the image.
extract_text() {
    python "$python_script_path/$python_script_name" \
    "$screenshot_dir/$screenshot_name" \
    "$python_script_path/$output_file_name"
}

# Copy the extracted text to clipboard using wl-copy and cliphist.
copy_to_wayland_clipboard() {
    cliphist store < "$python_script_path/$output_file_name"
    cliphist list | head -n 1 | cliphist decode | wl-copy
    rm "$python_script_path/$output_file_name"
}

# Copy the extracted text to clipboard using xclip.
copy_to_x11_clipboard() {
    xclip -selection clipboard -t text/plain -i "$python_script_path/$output_file_name"
    rm "$python_script_path/$output_file_name"
}

# Run the copy to clipboard functions based on the session type.
run_copy_to_clipboard() {
    if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
        copy_to_wayland_clipboard
    else
        copy_to_x11_clipboard
    fi
}

# Run the functions
main() {
    check_if_files_exist
    takescreenshot
    extract_text
    run_copy_to_clipboard
}

main
