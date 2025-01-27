"""
FileSaver Script

Author: Avery Harper
Date: January 26, 2025
Description: A utility script for saving content to a file with optional directory and filename parameters. 
             Supports automatic filename incrementation and customizable encoding.

Requirements:
- Python 3.7 or higher
- No external libraries required

Usage:
Run this script directly using the command line:
    python file_saver.py "Your content here" --directory /path/to/save --filename output.txt --encoding utf-8

Example:
    python file_saver.py "Hello, World!" --directory ./output --filename greeting.txt
"""

import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileSaver:
    @staticmethod
    def save(content: str, directory: Optional[str] = None, filename: Optional[str] = None, encoding: str = 'utf-8', return_path: bool = True) -> Optional[str]:
        """
        Saves content to a specified file in a specified directory.

        Parameters:
            content (str): The content to be saved in the file.
            directory (Optional[str]): The directory where the file will be saved. Defaults to the current directory.
            filename (Optional[str]): The name of the file. Defaults to "output.txt".
            encoding (str): The encoding to use when writing the file. Defaults to 'utf-8'.
            return_path (bool): Whether to return the file path after saving. Defaults to True.

        Returns:
            Optional[str]: The full path of the saved file if return_path is True, otherwise None.
        """
        if not content:
            logging.error("Content to save cannot be empty.")
            raise ValueError("Content cannot be empty.")

        directory = directory or os.getcwd()
        filename = filename or "output.txt"

        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # Handle file name incrementation
        file_path = os.path.join(directory, filename)
        base_name, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(directory, f"{base_name}_{counter}{ext}")
            counter += 1

        # Write the content to the file
        try:
            with open(file_path, 'w', encoding=encoding) as file:
                file.write(content)
            logging.info(f"File saved successfully at: {file_path}")
        except Exception as e:
            logging.error(f"An error occurred while saving the file: {e}")
            raise

        return file_path if return_path else None

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Save content to a file.")
    parser.add_argument("content", type=str, help="The content to save.")
    parser.add_argument("--directory", type=str, help="The directory to save the file in.", default=None)
    parser.add_argument("--filename", type=str, help="The filename to use.", default=None)
    parser.add_argument("--encoding", type=str, help="The encoding to use when saving the file.", default="utf-8")

    args = parser.parse_args()

    try:
        saved_path = FileSaver.save(
            args.content, directory=args.directory, filename=args.filename, encoding=args.encoding
        )
        if saved_path:
            logging.info(f"File saved at: {saved_path}")
    except Exception as e:
        logging.error(f"Failed to save the file: {e}")
