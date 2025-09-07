# ========================================================================================================================
# Author:
#     Mohamed Hussein Al-Adawy
# Version: 1.3.0
# Description:
#     OCR4Linux.py is a Python script that handles image preprocessing and text extraction using Tesseract OCR.
#     The script takes an input image, processes it for optimal OCR accuracy, and extracts text while preserving
#     line breaks and layout.
#
# Features:
#     - Image preprocessing (grayscale conversion, thresholding, noise removal)
#     - Text extraction with layout preservation
#     - Confidence-based filtering for improved accuracy
#     - Support for multiple image formats
#     - UTF-8 text output
#
# Dependencies:
#     - PIL (Python Imaging Library)
#     - pytesseract
#     - OpenCV (cv2)
#     - numpy
#
# Class Structure:
#     TesseractConfig:
#         - preprocess_image(): Enhances image quality for better OCR
#         - extract_text_with_lines(): Extracts text while preserving layout
#         - help(): Displays usage instructions
#         - main(): Orchestrates the OCR process
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


class TesseractConfig:
    """
    TesseractConfig is a class that configures and uses Tesseract OCR to extract text from images.

        langs (str): The languages to be used by Tesseract for OCR.
        custom_config (str): Custom configuration string for Tesseract.
        output_encoding (str): The encoding to be used for the output file.

    Methods:
        __init__(self, image_path: str, output_path: str):
            Initializes the TesseractConfig class with the provided image and output file paths.

        extract_text_with_lines(image: Image) -> str:
            Uses Tesseract OCR to extract text from the provided image, preserving line breaks.

        main() -> int:
            Main function to process the image and extract text. Performs validation, image processing,
            text extraction, and saves the extracted text to an output file. Returns 0 if successful, 1 otherwise.
    """

    def __init__(self, image_path: str, output_path: str, langs: str = None):
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
        self.available_langs = pytesseract.get_languages()

        # Use provided languages or default to all available languages
        if langs and langs.strip():
            self.langs = langs
            print(f"Using specified languages: {langs}", file=sys.stderr)
        else:
            self.langs = '+'.join(filter(None, self.available_langs)
                                  ) if self.available_langs else 'eng'
            print(
                f"Using all available languages: {self.langs}", file=sys.stderr)

        self.custom_config = f'--oem {self.oem_mode} --psm {self.psm_mode}'
        self.output_encoding = 'utf-8'

    def extract_text_with_lines(self, image: Image) -> str:
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
        self.version = "1.3.0"
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
            self.help()
            return 1
        return 2

    def list_available_languages(self) -> None:
        """
        Displays all available languages for Tesseract OCR.
        """
        langs = pytesseract.get_languages()
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
            int: Returns 1 if there is an error with the arguments or image path, otherwise returns the result of the TesseractConfig main function.
        """
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
        langs = None
        if len(sys.argv) >= 4 and sys.argv[3] == '--langs' and len(sys.argv) == 5:
            langs = sys.argv[4]
        elif len(sys.argv) == 4 and sys.argv[3].startswith('--langs='):
            langs = sys.argv[3].split('=', 1)[1]

        # Create an instance of the TesseractConfig class
        tesseract = TesseractConfig(sys.argv[1], sys.argv[2], langs)
        return tesseract.main()


if __name__ == "__main__":
    sys.exit(Program().main())
