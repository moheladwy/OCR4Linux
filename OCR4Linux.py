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
from PIL import Image
import pytesseract
import sys
import os
import cv2
import numpy as np


class TesseractConfig:
    def __init__(self):
        self.Args_num = 3
        self.script_name = sys.argv[0]
        self.image_path = sys.argv[1]
        self.output_path = sys.argv[2]

    def preprocess_image(self, image):
        """Preprocess image for better OCR accuracy"""
        # Convert to grayscale
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        # Apply thresholding
        thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # Noise removal
        denoised = cv2.medianBlur(thresh, 3)
        return Image.fromarray(denoised)

    def extract_text_with_lines(self, image):
        """Extract text while preserving line breaks"""
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

    def help(self):
        print(f"Usage: python {self.script_name} <image_path> <output_path>")
        print("Arguments:")
        print("  file_path: Path to the python script")
        print("  image_path: Path to the image file")
        print("  output_path: Path to the output text file")

    def main(self):
        # Check command line arguments
        if len(sys.argv) != self.Args_num or sys.argv[1] in ['-h', '--help']:
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
