# OCR4Linux

OCR4Linux is a versatile text extraction tool that allows you to take a screenshot of a selected area, extract text using OCR, and copy it to the clipboard. It supports both Wayland and X11 sessions and offers multiple language support.

**Note:** This script is currently only made for Arch Linux. It may work on other arch-based distributions, but it has not been tested yet.

## Motivation

I didn't find any easy tool in Linux that does the same thing as the PowerTool app in Windows. This motivated me to create OCR4Linux, a simple and efficient tool to capture screenshots, extract text, and copy it to the clipboard, all in one seamless process.

## Features

-   **Screenshot Capture**

    -   Wayland support via `grimblast`
    -   X11 support via `scrot`
    -   Configurable screenshot directory

-   **Text Extraction**

    -   Automatic language detection
    -   Multi-language OCR support
    -   Image preprocessing for better accuracy
    -   UTF-8 text output

-   **Clipboard Integration**

    -   Wayland: `wl-copy` and `cliphist`
    -   X11: `xclip`

-   **Additional Features**
    -   Optional screenshot retention
    -   Comprehensive logging system
    -   Command-line interface

## Requirements

### System Requirements

-   Arch Linux or arch-based distribution
-   Python 3.x
-   `yay` package manager (will be installed if needed)
-   `tesseract` OCR engine
-   `tesseract-data-eng` English language pack
-   `tesseract-data-ara` Arabic language pack
-   If you need any other language other than the above two, search for it using the command:

    ```sh
    sudo pacman -Ss tesseract-data-{lang}
    ```

### Python Dependencies

-   `python-pillow`
-   `python-pytesseract`

### Session-Specific Requirements

-   Wayland:
    -   `grimblast-git`
    -   `wl-clipboard`
    -   `cliphist`
    -   `rofi-wayland`
-   X11:
    -   `scrot`
    -   `xclip`
    -   `rofi`

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/moheladwy/OCR4Linux.git
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

### Command Line Arguments

---

#### OCR4Linux.sh

| Option   | Description                        | Default                      |
| -------- | ---------------------------------- | ---------------------------- |
| `-r`     | Remove screenshot after processing | `false`                      |
| `-d DIR` | Set screenshot directory           | `$HOME/Pictures/screenshots` |
| `-l`     | Keep logs                          | `false`                      |
| `-h`     | Show help message                  | -                            |

#### OCR4Linux.py

| Option             | Description                  | Required |
| ------------------ | ---------------------------- | -------- |
| `image_path`       | Path to input image          | Yes      |
| `output_path`      | Path to save extracted text  | Yes      |
| `-l, --list-langs` | List available OCR languages | No       |
| `-h, --help`       | Show help message            | No       |

### Examples

---

#### Using OCR4Linux.sh

```sh
# Basic usage
./OCR4Linux.sh

# Save logs and remove screenshot after processing
./OCR4Linux.sh -l -r

# Custom screenshot directory with logging
./OCR4Linux.sh -d ~/Documents/screenshots -l

# Show help
./OCR4Linux.sh -h
```

#### Using OCR4Linux.py

```sh
# Basic usage
python OCR4Linux.py input.png output.txt

# List available languages
python OCR4Linux.py --list-langs

# Show help
python OCR4Linux.py --help
```

## Tips

-   You can create a keyboard shortcut to run the script for easy access.
    ### Example for `Hyprland` users:
    -   put the following lines in your `hyprland.conf` file:
        ```conf
        $OCR4Linux = ~/.config/OCR4Linux/OCR4Linux.sh
        bind = $mainMod SHIFT, E, exec, $OCR4Linux # OCR4Linux script
        ```
    ### Example for `dwm` users:
    -   put the following lines in your `config.h` file:
        ```c
        static const char *ocr4linux[] = { "sh", "-c", "~/.config/OCR4Linux/OCR4Linux.sh", NULL };
        { MODKEY | ShiftMask, XK_e, spawn, {.v = ocr4linux } },  // OCR4Linux script
        ```

## Files

-   [OCR4Linux.py](https://github.com/moheladwy/OCR4Linux/blob/main/OCR4Linux.py): Python script to preprocess the image and extract text using `tesseract`.
-   [OCR4Linux.sh](https://github.com/moheladwy/OCR4Linux/blob/main/OCR4Linux.sh): Shell script to take a screenshot, pass it to the python script, get the extracted text from the python script, and copy it to the clipboard.
-   [setup.sh](https://github.com/moheladwy/OCR4Linux/blob/main/setup.sh): Shell script to install the required packages and copy the necessary files to the configuration directory (run this script the first time you clone the repository only).

## Contributing

We welcome contributions from the community to help improve OCR4Linux and make it available for all Linux users and distributions. Whether it's reporting bugs, suggesting new features, or submitting patches, your help is greatly appreciated. Please check out our [contributing guidelines](https://github.com/moheladwy/OCR4Linux/blob/main/CONTRIBUTING.md) to get started.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/moheladwy/OCR4Linux/blob/main/LICENSE) file for more details.
