# ========================================================================================================================
# Author:
#     Mohamed Hussein Al-Adawy
# Version: 1.5.0
# Description:
#     OCR4Linux.py is a Python script that extracts text from an image using Tesseract OCR.
#     The script takes an input image and extracts text from it while preserving line breaks
#     and layout.
#
# Features:
#     - Text extraction with layout preservation
#     - Selectable OCR languages, defaulting to every language installed on the system
#     - Support for multiple image formats
#     - UTF-8 text output
#
# Dependencies:
#     - PIL (Python Imaging Library)
#     - pytesseract
#
# Class Structure:
#     TesseractConfig:
#         - extract_text_with_lines(): Extracts text while preserving layout
#         - main(): Orchestrates the OCR process
#     Program:
#         - help(): Displays usage instructions
#         - check_arguments(): Validates the command-line arguments
#         - main(): Entry point that wires everything together
#
# Usage:
#     python OCR4Linux.py <image_path> <output_path>
#
# Example:
#     python OCR4Linux.py screenshot.png output.txt
# ========================================================================================================================

import sys
import os
from PIL import Image
import pytesseract


class TesseractUnavailableError(RuntimeError):
    """Raised when Tesseract cannot be reached or is misconfigured."""


def get_available_languages() -> list:
    """
    Queries Tesseract for the languages installed on this system.

    Returns:
        list: The names of the installed languages.

    Raises:
        TesseractUnavailableError: If the tesseract binary is missing or its
            tessdata directory cannot be read.
    """
    try:
        return [lang for lang in pytesseract.get_languages() if lang]
    except Exception as e:
        raise TesseractUnavailableError(
            "Could not query Tesseract for its installed languages. Make sure "
            "the 'tesseract' binary is installed and that TESSDATA_PREFIX "
            f"points to a valid tessdata directory. Details: {e}") from e


class TesseractConfig:
    """
    TesseractConfig is a class that configures and uses Tesseract OCR to extract text from images.

        langs (str): The languages to be used by Tesseract for OCR.
        custom_config (str): Custom configuration string for Tesseract.
        output_encoding (str): The encoding to be used for the output file.

    Methods:
        __init__(self, image_path: str, output_path: str):
            Initializes the TesseractConfig class with the provided image and output file paths.

        validate_langs(langs: str) -> str:
            Checks that every requested language is installed, raising ValueError otherwise.

        extract_text_with_lines(image: Image) -> str:
            Uses Tesseract OCR to extract text from the provided image, preserving line breaks.

        main() -> int:
            Main function to process the image and extract text. Performs validation, image processing,
            text extraction, and saves the extracted text to an output file. Returns 0 if successful, 1 otherwise.
    """

    def __init__(self, image_path: str, output_path: str, langs: str | None = None):
        """
        Initializes the OCR4Linux class with command-line arguments.

        Attributes:
            image_path (str): The path to the input image file.
            output_path (str): The path to the output file where results will be saved.
            langs (str): The languages to be used by Tesseract for OCR (optional).
            oem_mode (int): The OCR Engine Mode (OEM) for Tesseract.
            psm_mode (int): The Page Segmentation Mode (PSM) for Tesseract.
            custom_config (str): Custom configuration string for Tesseract.
            output_encoding (str): The encoding to be used for the output file.
        """
        self.image_path = image_path
        self.output_path = output_path
        self.oem_mode = 3  # Default LSTM engine
        self.psm_mode = 6  # Uniform block of text
        self.available_langs = get_available_languages()

        # Use provided languages or default to all available languages
        if langs and langs.strip():
            self.langs = self.validate_langs(langs)
            print(f"Using specified languages: {self.langs}", file=sys.stderr)
        else:
            self.langs = '+'.join(
                self.available_langs) if self.available_langs else 'eng'
            print(
                f"Using all available languages: {self.langs}", file=sys.stderr)

        self.custom_config = f'--oem {self.oem_mode} --psm {self.psm_mode}'
        self.output_encoding = 'utf-8'

    def validate_langs(self, langs: str) -> str:
        """
        Checks that every language in a '+' separated string is installed.

        Args:
            langs: A '+' separated list of Tesseract language names.

        Returns:
            str: The normalized '+' separated language string.

        Raises:
            ValueError: If the string is empty or names a language that is not
                installed on this system.
        """
        requested = [lang for lang in langs.split('+') if lang.strip()]
        if not requested:
            raise ValueError("No languages were specified")

        missing = [
            lang for lang in requested if lang not in self.available_langs]
        if missing:
            raise ValueError(
                f"Language(s) not installed: {', '.join(missing)}. "
                f"Available languages: {', '.join(self.available_langs)}")

        return '+'.join(requested)

    def extract_text_with_lines(self, image: Image.Image) -> str:
        """
        This method uses Tesseract OCR to extract text from the provided image.

        Args:
            image: The image from which to extract text. This should be a format
                   supported by the pytesseract library.

        Returns:
            A string containing the extracted text with line breaks preserved.
        """
        return pytesseract.image_to_string(
            image=image, lang=self.langs, config=self.custom_config)

    def main(self) -> int:
        """
        Main function to process the image and extract text.

        This function performs the following steps:
        1. Extracts text from the processed image while preserving line breaks.
        2. Saves the extracted text to an output file.

        Returns:
            int: 0 if text extraction is successful, 1 otherwise.
        """
        try:
            # Open and process the image
            with Image.open(self.image_path) as image:
                # Extract text with line preservation
                extracted_text = self.extract_text_with_lines(image)

                # Save the extracted text to a file
                with open(self.output_path, 'w', encoding=self.output_encoding) as file:
                    file.write(extracted_text)

                return 0

        except Exception as e:
            print(f"Error processing image because: {str(e)}")
            return 1


class Program:
    def __init__(self):
        """
        Initializes the OCR4Linux class with the following attributes:
        - args_num: Number of arguments expected by the script.
        - author: Author of the script.
        - email: Author's email address.
        - github: URL to the GitHub repository.
        - version: Version of the script.
        - description: Brief description of the script's functionality.
        - useges: List of usage examples for the script.
        - examples: List of example commands for using the script.
        - arguments: List of arguments that the script accepts with their descriptions.
        """
        self.args_num = 3
        self.author = "Mohamed Hussein Al-Adawy"
        self.email = "mohamed.h.eladwy@gmail.com"
        self.github = "https://github.com/moheladwy/OCR4Linux"
        self.version = "1.5.0"
        self.description = \
            "    OCR4Linux.py is a Python script that handles image preprocessing\n" + \
            "    and text extraction using Tesseract OCR. The script takes an input\n" + \
            "    based on the language in the image."
        self.useges = [
            "python OCR4Linux.py <image_path> <output_path> [--langs <languages>]",
            "python OCR4Linux.py [-l | --list-langs]",
            "python OCR4Linux.py [-h | --help]"
        ]
        self.examples = [
            "python OCR4Linux.py screenshot.png output.txt",
            "python OCR4Linux.py screenshot.png output.txt --langs eng+fra+deu",
            "python OCR4Linux.py -l",
            "python OCR4Linux.py -h"
        ]
        self.arguments = [
            "file_path:         Path to the python script",
            "image_path:        Path to the image file",
            "output_path:       Path to the output text file",
            "--langs:           Specify languages for OCR (e.g., eng+fra+deu)",
            "-l, --list-langs:  List all available languages for OCR in the system",
            "-h, --help:        Display this help message, then exit"
        ]

    def help(self) -> None:
        """
        Prints the usage instructions for the OCR4Linux script.

        This method displays the correct way to run the script, including the required
        arguments and their descriptions. It also provides examples of how to use the script.
        """
        print("OCR4Linux - OCR script for Linux using Tesseract")
        print(f"Version: {self.version}")
        print(f"Author:  {self.author}")
        print(f"Email:   {self.email}")
        print(f"GitHub:  {self.github}")
        print()
        print("Description:")
        print(self.description)
        print()
        print("Usage:")
        for usege in self.useges:
            print(f"    - {usege}")
        print()
        print("Example:")
        for example in self.examples:
            print(f"    - {example}")
        print()
        print("Arguments:")
        for argument in self.arguments:
            print(f"    {argument}")

    def check_arguments(self) -> int:
        """
        Checks the command line arguments for validity.

        Handles the following options:
        - Standard usage: <image_path> <output_path> [--langs <languages>]
        - Help: -h or --help
        - List languages: -l or --list-langs

        Returns:
            int: 0 if help/list was shown, 1 if error, 2 if valid arguments for processing.
        """
        if len(sys.argv) == 2 and sys.argv[1] in ['-l', '--list-langs']:
            self.list_available_languages()
            return 0
        elif len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
            self.help()
            return 0
        elif len(sys.argv) < self.args_num or len(sys.argv) > 5:
            # Valid patterns:
            # 3 args: script image_path output_path
            # 4 args: script image_path output_path --langs=languages
            # 5 args: script image_path output_path --langs languages
            print(
                f"Error: expected 2 to 4 arguments, got {len(sys.argv) - 1}",
                file=sys.stderr)
            self.help()
            return 1
        return 2

    def parse_langs(self) -> tuple:
        """
        Parses the optional --langs argument from the trailing arguments.

        Accepts either '--langs <languages>' or '--langs=<languages>' and
        rejects anything else instead of silently ignoring it.

        Returns:
            tuple: (ok, langs) where ok is False when the trailing arguments
                are malformed and langs is None when --langs was not given.
        """
        trailing = sys.argv[3:]

        if not trailing:
            return True, None

        if len(trailing) == 1:
            if trailing[0] == '--langs':
                print("Error: --langs requires a value (e.g. --langs eng+ara)",
                      file=sys.stderr)
                return False, None
            if not trailing[0].startswith('--langs='):
                print(f"Error: unrecognized argument '{trailing[0]}'",
                      file=sys.stderr)
                return False, None
            langs = trailing[0].split('=', 1)[1]
        elif trailing[0] == '--langs':
            langs = trailing[1]
        else:
            print(f"Error: unrecognized argument '{trailing[0]}'",
                  file=sys.stderr)
            return False, None

        if not langs.strip():
            print("Error: --langs requires a non-empty value (e.g. eng+ara)",
                  file=sys.stderr)
            return False, None

        return True, langs

    def list_available_languages(self) -> None:
        """
        Displays all available languages for Tesseract OCR.
        """
        langs = get_available_languages()
        if not langs:
            print("Error: No languages found")
            return

        print("Available languages for OCR:")
        for lang in langs:
            print(f"  - {lang}")

    def check_image_path(self, image_path: str) -> bool:
        """
        Checks if the specified image file exists.

        Args:
            image_path: The path to the image file to be checked.

        Returns:
            bool: True if the image file exists, False otherwise.
        """
        if not os.path.exists(image_path):
            print(f"Error: File '{image_path}' not found")
            return False
        return True

    def main(self):
        """
        Main function to execute the OCR process.

        This function performs the following steps:
        1. Checks if the correct number of arguments is provided.
        2. Verifies if the image file exists.
        3. Parses language arguments if provided.
        4. Creates an instance of the TesseractConfig class and runs the OCR process.

        Returns:
            int: Returns 1 if there is an error with the arguments, the image path,
            the requested languages or the Tesseract installation, otherwise returns
            the result of the TesseractConfig main function.
        """
        try:
            # Check if the correct number of arguments is provided
            result = self.check_arguments()
            if result == 1:
                return 1
            elif result == 0:
                return 0

            # Check if the image file exists
            if not self.check_image_path(sys.argv[1]):
                return 1

            # Parse language arguments
            ok, langs = self.parse_langs()
            if not ok:
                self.help()
                return 1

            # Create an instance of the TesseractConfig class
            tesseract = TesseractConfig(sys.argv[1], sys.argv[2], langs)
            return tesseract.main()

        except TesseractUnavailableError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1


if __name__ == "__main__":
    sys.exit(Program().main())
