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

# Define the required packages.
sys_requirements=(
    tesseract
    tesseract-data-eng
    tesseract-data-ara
    python
    python-numpy
    python-pillow
    python-pytesseract
    python-opencv
)
wayland_session_apps=(
    grimblast-git
    wl-clipboard
    cliphist
    rofi-wayland
)
x11_session_apps=(
    xclip
    scrot
    rofi
)

# Check if yay is installed.
check_yay() {
    if ! command -v yay &> /dev/null; then
        read -p "yay is not installed. Do you want to install yay? (y/n): " choice
        if [ "$choice" = "y" ]; then
            sudo pacman -S --needed --noconfirm git base-devel
            git clone https://aur.archlinux.org/yay.git
            cd yay
            makepkg -si --noconfirm
        else
            echo "Please install yay first!"
            return 1
        fi
    fi
}

# Install the required packages.
install_requirements() {
    yay -S --noconfirm --needed "${sys_requirements[@]}"

    if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
        yay -S --noconfirm --needed "${wayland_session_apps[@]}"
    else
        yay -S --noconfirm --needed "${x11_session_apps[@]}"
    fi
}

# Main function.
main() {
    check_yay
    install_requirements

    # Copy the script to the user's home directory.
    mkdir -p "$HOME/.config/OCR4Linux"
    cp -r ./* "$HOME/.config/OCR4Linux"
}

main