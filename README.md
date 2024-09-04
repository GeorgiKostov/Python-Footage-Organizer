# sortgameboy.py - GBC Organizer
This script allows users to manage their collection of GBC games. It searches through a specified source directory for GBC game files and allows the user to selectively copy them to a destination directory. This tool is especially useful for organizing and archiving Gameboy Color games based on specific search criteria.

## Features
- **Interactive Search**: Users can enter the name of a game, and the script will find all `.gbc` files that match the name (case insensitive).
- **Selective Copying**: After searching, the script displays a list of matching files. Users can specify one or more files to copy by entering their corresponding numbers.
- **Multi-Selection**: Users can select multiple files at once by entering their numbers separated by commas.
- **Automatic Directory Handling**: The script automatically creates the destination directory if it does not exist.

## Usage
1. **Prepare Directories**: Ensure you have a directory named `gameboyroms` in the same location as this script containing your `.gbc` files.
2. **Run the Script**: Execute the script by running `python sortgameboy.py` from your command line or terminal.
3. **Enter Game Names**: Input the name of the game you are looking for, or part of it, to find matching `.gbc` files.
4. **Select Files to Copy**: After the files are listed, enter the numbers of the files you wish to copy, separated by commas. Enter `0` to finish the selection for the current game and start a new search or to quit the program.

## Requirements
- Python 3.x installed on your machine.
- Gameboy Color ROM files placed within a directory named `gameboyroms` located in the same directory as the script.

## Exiting the Program
To exit the program, simply enter `0` when prompted to enter a game name.


# sortphotos.py - Media File Organizer
This Python script is designed to help organize media files (images and videos) by automatically sorting them into directories based on the date the media was created or taken. It leverages EXIF data for images and file creation dates for videos. The script also provides functionalities to delete specific file types (JSON) and allows user interaction for selective processing.

## Features
- **Automatic Sorting**: Sorts media files into folders structured by year and month based on the media's creation date.
- **EXIF Data Extraction**: For images, the script attempts to extract the 'Date Taken' from the EXIF data.
- **Fallback Date Handling**: If EXIF data is not available or applicable, the script uses Windows file properties or filesystem's creation date.
- **Selective Processing**: Users can choose to process all media within the script's directory, select a specific folder, or delete all JSON files.
- **Support for Multiple Formats**: Handles common image formats like JPG, PNG, GIF, and BMP, as well as video formats like MP4, AVI, MOV, and MKV.

## Usage
1. **Setup**: Place the script in the root directory where your media files are stored. Ensure that the directory structure contains subdirectories with the media files to be organized.
2. **Run the Script**:
    - Open a command line interface.
    - Navigate to the directory containing the script.
    - Run the script using Python by typing: `sortphotos.py`.
3. **Follow Prompts**:
    - Choose to process all media files, select a specific folder for processing, or delete all JSON files within the directory.
    - The script will provide updates on the number of files processed, copied, and skipped.

## Requirements
- Python 3.x
- `Pillow` library for handling images
- `pywin32` library for accessing Windows file properties
- `python-dateutil` for parsing dates

## Installation of Dependencies
Install the required Python libraries using pip:
```bash
pip install Pillow pywin32 python-dateutil

