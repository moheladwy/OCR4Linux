#!/bin/bash
# ========================================================================================================================
# Author:
#     Mohamed Hussein Al-Adawy
# Version: 1.4.0
# Description:
#     This setup script installs and configures OCR4Linux and its dependencies.
#     It handles the installation of:
#       1. System requirements (tesseract, python packages)
#       2. Session-specific tools:
#          - Wayland: grimblast, wl-clipboard, cliphist, rofi-wayland
#          - X11: xclip, scrot, rofi
#
# Features:
#     - Automatic detection and installation of AUR helper (yay)
#     - Session-aware installation (Wayland/X11)
#     - Configures necessary Python dependencies
#     - Sets up required OCR language packs
#
# Requirements:
#     - Arch Linux or Arch-based distribution
#     - Internet connection for package downloads
#     - sudo privileges for package installation
#
# Usage:
#     chmod +x setup.sh
#     ./setup.sh
#     Follow the prompts to install dependencies
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
    echo "Checking for yay AUR helper..."
    if ! command -v yay &>/dev/null; then
        read -r -p "yay is not installed. Do you want to install yay? (y/n): " choice
        if [ "$choice" = "y" ]; then
            sudo pacman -S --needed --noconfirm git base-devel
            git clone https://aur.archlinux.org/yay.git
            cd yay || exit
            makepkg -si --noconfirm
            echo "yay has been installed successfully."
        else
            echo "Please install yay first!"
            return 1
        fi
    else
        echo "yay is already installed."
    fi
}

# Install the required packages.
install_requirements() {
    echo "Installing system requirements..."
    yay -S --noconfirm --needed "${sys_requirements[@]}"

    if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
        echo "Installing Wayland session applications..."
        yay -S --noconfirm --needed "${wayland_session_apps[@]}"
    else
        echo "Installing X11 session applications..."
        yay -S --noconfirm --needed "${x11_session_apps[@]}"
    fi

    echo "All requirements have been installed successfully."
}

# Main function.
main() {
    echo "========================================================================================================"
    echo "Starting OCR4Linux setup..."
    echo "========================================================================================================"
    check_yay
    echo "========================================================================================================"
    install_requirements
    echo "========================================================================================================"
    # Copy the script to the user's home directory.
    echo "Setting up OCR4Linux configuration..."
    mkdir -p "$HOME/.config/OCR4Linux"
    cp -r ./* "$HOME/.config/OCR4Linux"
    echo "OCR4Linux has been set up successfully in $HOME/.config/OCR4Linux"
    echo "Setup completed. You can now use OCR4Linux."
    echo "========================================================================================================"
}

main
