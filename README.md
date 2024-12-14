# OCR4Linux

OCR4Linux is a tool that allows you to take a screenshot of a selected area, extract the text from the image, and copy it to the clipboard. It supports both Wayland and X11 sessions and uses various tools to achieve its functionality.
Note: This script is currently only made for Arch Linux. It may work on other arch-based distributions, but it has not been tested yet.

## Motivation

I didn't find any easy tool in Linux that does the same thing as the PowerTool app in Windows. This motivated me to create OCR4Linux, a simple and efficient tool to capture screenshots, extract text, and copy it to the clipboard, all in one seamless process.

## Features

-   Takes screenshots using `grimblast` for Wayland and `scrot` for X11.
-   Uses a pytesseract python script to preprocess the image and extract text.
-   Copies the extracted text to the clipboard using `wl-copy` and `cliphist` for Wayland and `xclip` for X11.

## Requirements

The following packages are required to be installed:

-   `python`
    -   `python-numpy`
    -   `python-pillow`
    -   `python-pytesseract`
    -   `python-opencv`
-   `tesseract`
-   `grimblast` for `wayland` or `scrot` for `x11`
-   `wl-copy` and `cliphist` for `wayland` or `xclip` for `x11`

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/OCR4Linux.git
    cd OCR4Linux
    ```

2. Run the setup script to install the required packages and copy the necessary files to the configuration directory:

    ```sh
    chmod +x setup.sh
    ./setup.sh
    ```

## Usage

1. Run the main script to take a screenshot, extract text, and copy it to the clipboard:

    ```sh
    chmod +x OCR4Linux.sh
    ./OCR4Linux.sh
    ```

2. The script will take a screenshot of the selected area, extract the text from the image, and copy it to the clipboard.

## Tips

-   You can customize the script to suit your needs by changing the screenshot tool, text extraction method, or clipboard manager.
-   You can create a keyboard shortcut to run the script for easy access.
    ### Example for `Hyprland` users:
    -   put the following lines in your `hyprland.conf` file:
        ```
        $OCR4Linux = ~/.config/OCR4Linux/OCR4Linux.sh
        bind = $mainMod SHIFT, E, exec, $OCR4Linux # OCR4Linux script
        ```
    ### Example for `dwm` users:
    -   put the following lines in your `config.h` file:
        ```
        static const char *ocr4linux[] = { "sh", "-c", "~/.config/OCR4Linux/OCR4Linux.sh", NULL };
        { MODKEY | ShiftMask, XK_e, spawn, {.v = ocr4linux } }, // OCR4Linux script
        ```

## Files

-   [OCR4Linux.py](https://github.com/moheladwy/OCR4Linux/blob/main/OCR4Linux.py): Python script to preprocess the image and extract text using `tesseract`.
-   [OCR4Linux.sh](https://github.com/moheladwy/OCR4Linux/blob/main/OCR4Linux.sh): Shell script to take a screenshot, extract text, and copy it to the clipboard.
-   [setup.sh](https://github.com/moheladwy/OCR4Linux/blob/main/setup.sh): Shell script to install the required packages and copy the necessary files to the configuration directory.

## Contributing

We welcome contributions from the community to help improve OCR4Linux and make it available for all Linux users and distributions. Whether it's reporting bugs, suggesting new features, or submitting patches, your help is greatly appreciated. Please check out our [contributing guidelines](https://github.com/moheladwy/OCR4Linux/blob/main/CONTRIBUTING.md) to get started.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/moheladwy/OCR4Linux/blob/main/LICENSE) file for more details.
