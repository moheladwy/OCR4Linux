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

    -   Interactive language selection via `rofi`
    -   Multi-language OCR support with custom language combinations
    -   Automatic language detection fallback
    -   Image preprocessing for better accuracy
    -   UTF-8 text output

-   **Clipboard Integration**

    -   Wayland: `wl-copy` and `cliphist`
    -   X11: `xclip`

-   **Additional Features**
    -   Interactive language selection menu
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

**Note:** `rofi` is required for the interactive language selection feature.

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

2. The script will:
    - **With `--lang` option**: Use specified languages directly (bypasses rofi menu)
    - **Without `--lang` option**: Display an interactive language selection menu via `rofi`
    - Allow you to select one or multiple languages for OCR processing
    - Take a screenshot of the selected area after language selection
    - Extract text from the image using the selected languages
    - Copy the extracted text to the clipboard### Language Selection

You have two options for language selection:

#### Option 1: Command Line (Direct)

Specify languages directly using the `--lang` option:

-   `--lang all` - Use all available languages
-   `--lang eng` - Use English only
-   `--lang eng+ara+fra` - Use multiple specific languages

#### Option 2: Interactive Menu (Rofi)

When you run the script without `--lang`, a `rofi` menu will appear with:

-   **ALL**: Select all available languages
-   **Individual languages**: Choose specific languages (e.g., eng, ara, fra, deu)
-   **Multi-select**: Hold `Ctrl` and click to select multiple languages

The selected languages will be used by Tesseract for more accurate text recognition in multi-language documents.

## Workflow

The complete OCR4Linux workflow:

1. **Language Selection**:
    - Command-line specified languages (with `--lang`) OR
    - Interactive rofi menu displays available languages (without `--lang`)
2. **Language Processing**: Selected languages are validated and formatted
3. **Screenshot Capture**: Area selection and image capture
4. **OCR Processing**: Text extraction using selected languages
5. **Clipboard Integration**: Extracted text copied to system clipboard
6. **Cleanup**: Optional screenshot removal and logging

### Command Line Arguments

---

#### OCR4Linux.sh

| Option             | Description                           | Default                      |
| ------------------ | ------------------------------------- | ---------------------------- |
| `-r`               | Remove screenshot after processing    | `false`                      |
| `-d DIR`           | Set screenshot directory              | `$HOME/Pictures/screenshots` |
| `-l`               | Keep logs                             | `false`                      |
| `--lang LANGUAGES` | Specify OCR languages (bypasses rofi) | Interactive selection        |
| `-h`               | Show help message                     | -                            |

**Language Format for `--lang`**:

-   Use `all` for all available languages
-   Use `+` to separate multiple languages (e.g., `eng+ara+fra`)
-   Single languages: `eng`, `ara`, `fra`, etc.

#### OCR4Linux.py

| Option                | Description                  | Required |
| --------------------- | ---------------------------- | -------- |
| `image_path`          | Path to input image          | Yes      |
| `output_path`         | Path to save extracted text  | Yes      |
| `--langs <languages>` | Specify languages for OCR    | No       |
| `-l, --list-langs`    | List available OCR languages | No       |
| `-h, --help`          | Show help message            | No       |

**Language Format**: Use `+` to separate multiple languages (e.g., `eng+ara+fra`)

### Examples

---

#### Using OCR4Linux.sh

```sh
# Basic usage (shows interactive rofi menu)
./OCR4Linux.sh

# Direct language specification (bypasses rofi)
./OCR4Linux.sh --lang eng
./OCR4Linux.sh --lang all
./OCR4Linux.sh --lang eng+ara+fra

# Save logs and remove screenshot after processing
./OCR4Linux.sh -l -r

# Custom screenshot directory with logging
./OCR4Linux.sh -d ~/Documents/screenshots -l

# Combine language specification with other options
./OCR4Linux.sh --lang eng -l -r
./OCR4Linux.sh --lang all -d ~/screenshots -l

# Show help
./OCR4Linux.sh -h
```

#### Using OCR4Linux.py

```sh
# Basic usage (uses all available languages)
python OCR4Linux.py input.png output.txt

# Specify single language
python OCR4Linux.py input.png output.txt --langs eng

# Specify multiple languages
python OCR4Linux.py input.png output.txt --langs eng+ara+fra

# List available languages
python OCR4Linux.py --list-langs

# Show help
python OCR4Linux.py --help
```

## Tips

-   **Language Selection Options**:

    -   **Command Line**: Use `--lang` for automated/scripted usage

        -   `--lang all` for maximum compatibility
        -   `--lang eng` for English-only documents
        -   `--lang eng+ara` for bilingual documents

    -   **Interactive Menu**: Run without `--lang` for manual selection
        -   Select "ALL" to use all available languages
        -   Select specific languages for better performance
        -   Use `Ctrl+Click` to select multiple languages
        -   Press `Escape` to cancel the operation

-   **Performance Optimization**:

    -   Use fewer specific languages for faster processing
    -   Use `--lang all` only when document language is unknown
    -   Command-line specification is faster than interactive selection

-   **Keyboard Shortcuts**: You can create a keyboard shortcut to run the script for easy access.

    ### Example for `Hyprland` users:

    -   put the following lines in your `hyprland.conf` file:

        ```conf
        $OCR4Linux = ~/.config/OCR4Linux/OCR4Linux.sh
        $OCR4Linux_ENG = ~/.config/OCR4Linux/OCR4Linux.sh --lang eng

        bind = $mainMod SHIFT, E, exec, $OCR4Linux # OCR4Linux with interactive selection
        bind = $mainMod SHIFT, T, exec, $OCR4Linux_ENG # OCR4Linux with English only
        ```

    ### Example for `dwm` users:

    -   put the following lines in your `config.h` file:

        ```c
        static const char *ocr4linux[] = { "sh", "-c", "~/.config/OCR4Linux/OCR4Linux.sh", NULL };
        static const char *ocr4linux_eng[] = { "sh", "-c", "~/.config/OCR4Linux/OCR4Linux.sh --lang eng", NULL };

        { MODKEY | ShiftMask, XK_e, spawn, {.v = ocr4linux } },      // OCR4Linux interactive
        { MODKEY | ShiftMask, XK_t, spawn, {.v = ocr4linux_eng } },  // OCR4Linux English only
        ```

-   **Language Optimization**: For best results:
    -   Select only the languages present in your document
    -   Use fewer languages for better performance
    -   Install additional Tesseract language packs as needed

## Files

-   [OCR4Linux.py](https://github.com/moheladwy/OCR4Linux/blob/main/OCR4Linux.py): Python script to preprocess the image and extract text using `tesseract` with support for custom language selection.
-   [OCR4Linux.sh](https://github.com/moheladwy/OCR4Linux/blob/main/OCR4Linux.sh): Shell script that provides both interactive language selection via rofi and direct command-line language specification, takes a screenshot, passes it to the python script with selected languages, gets the extracted text, and copies it to the clipboard.
-   [setup.sh](https://github.com/moheladwy/OCR4Linux/blob/main/setup.sh): Shell script to install the required packages and copy the necessary files to the configuration directory (run this script the first time you clone the repository only).

## Contributing

We welcome contributions from the community to help improve OCR4Linux and make it available for all Linux users and distributions. Whether it's reporting bugs, suggesting new features, or submitting patches, your help is greatly appreciated. Please check out our [contributing guidelines](https://github.com/moheladwy/OCR4Linux/blob/main/CONTRIBUTING.md) to get started.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/moheladwy/OCR4Linux/blob/main/LICENSE) file for more details.
