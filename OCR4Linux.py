# ========================================================================================================================
# Author:
#     Mohamed Hussein Al-Adawy
# Version: 1.1.0
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
import cv2
import numpy as np


class TesseractConfig:
    """
    TesseractConfig is a class that provides functionality to preprocess images,
    and extract text from them using Tesseract OCR.

    Methods:
        __init__():
            Initializes the TesseractConfig instance with command line arguments.

        preprocess_image(image):
            Preprocesses the given image to improve OCR accuracy.
            Args:
                image (PIL.Image): The image to preprocess.
            Returns:
                PIL.Image: The preprocessed image.

        extract_text_with_lines(image):
            Extracts text from the given image while preserving line breaks.
            Args:
                image (PIL.Image): The image from which to extract text.
            Returns:
                str: The extracted text with line breaks preserved.

        help():
            Prints the usage information for the script.

        main():
            The main method that processes the image and extracts text.
            Returns:
                int: 0 if successful, 1 otherwise.
    """

    def __init__(self):
        """
        Initializes the OCR4Linux class with command-line arguments.

        Attributes:
            args_num (int): The number of expected command-line arguments.
            script_name (str): The name of the script being executed.
            image_path (str): The path to the input image file.
            output_path (str): The path to the output file where results will be saved.
        """
        self.args_num = 3
        self.script_name = sys.argv[0]
        self.image_path = sys.argv[1]
        self.output_path = sys.argv[2]

    def preprocess_image(self, image) -> Image:
        """
        Preprocess image for better OCR accuracy.

        This function converts the input image to grayscale, applies thresholding 
        to binarize the image, and removes noise using a median blur filter.

        Args:
            image (PIL.Image.Image): The input image to preprocess.

        Returns:
            PIL.Image.Image: The preprocessed image.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        # Apply thresholding
        thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # Noise removal
        denoised = cv2.medianBlur(thresh, 3)
        return Image.fromarray(denoised)

    def extract_text_with_lines(self, image: Image) -> str:
        """
        Extract text from an image while preserving line breaks.

        This method uses Tesseract OCR to extract text from the provided image,
        preserving the layout and line breaks. It filters out low-confidence
        results to improve the accuracy of the extracted text.

        Args:
            image: The image from which to extract text. This should be a format
                   supported by the pytesseract library.

        Returns:
            A string containing the extracted text with line breaks preserved.
        """
        # Get image dimensions
        custom_config = r'--oem 3 --psm 6'
        # Extract text with layout preservation
        data = pytesseract.image_to_data(
            image, config=custom_config, output_type=pytesseract.Output.DICT)

        # Group text by line
        lines = {}
        for i, _ in enumerate(data['level']):
            if int(data['conf'][i]) > 60:  # Filter low confidence results
                page_num = data['page_num'][i]
                block_num = data['block_num'][i]
                par_num = data['par_num'][i]
                line_num = data['line_num'][i]

                key = f"{page_num}_{block_num}_{par_num}_{line_num}"
                if key not in lines:
                    lines[key] = []
                lines[key].append(data['text'][i])

        # Join text preserving line breaks
        return '\n'.join(' '.join(line).strip() for line in lines.values() if ''.join(line).strip())

    def help(self) -> None:
        """
        Prints the usage instructions for the OCR4Linux script.

        This method displays the correct way to run the script, including the required
        arguments and their descriptions.

        Usage:
            python <script_name> <image_path> <output_path>

        Arguments:
            file_path: Path to the python script
            image_path: Path to the image file
            output_path: Path to the output text file
        """
        print(f"Usage: python {self.script_name} <image_path> <output_path>")
        print("Arguments:")
        print("  file_path: Path to the python script")
        print("  image_path: Path to the image file")
        print("  output_path: Path to the output text file")

    def main(self) -> int:
        """
        Main function to process the image and extract text.

        This function performs the following steps:
        1. Checks command line arguments for validity.
        2. Verifies if the specified image file exists.
        3. Opens and processes the image.
        4. Extracts text from the processed image while preserving line breaks.
        5. Saves the extracted text to an output file.

        Returns:
            int: 0 if text extraction is successful, 1 otherwise.
        """
        # Check command line arguments
        if len(sys.argv) != self.args_num or sys.argv[1] in ['-h', '--help']:
            self.help()
            return 1

        # Check if file exists
        if not os.path.exists(self.image_path):
            print(f"Error: File '{self.image_path}' not found")
            return 1

        try:
            # Open and process the image
            with Image.open(self.image_path) as image:
                # Preprocess the image
                processed_image = self.preprocess_image(image)

                # Extract text with line preservation
                extracted_text = self.extract_text_with_lines(processed_image)

                # Save the extracted text to a file
                with open(self.output_path, 'w', encoding='utf-8') as file:
                    file.write(extracted_text)

                print("Text extraction completed successfully")
                return 0

        except Exception as e:
            print(f"Error processing image because: {str(e)}")
            return 1


if __name__ == "__main__":
    sys.exit(TesseractConfig().main())
