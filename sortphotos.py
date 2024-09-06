import os
import shutil
from datetime import datetime
from PIL import Image, UnidentifiedImageError
import re

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv']

def list_directories(path):
    """List all directories at a given path."""
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def get_image_exif_date(path):
    """Attempt to get the 'Date Taken' from image EXIF data."""
    try:
        image = Image.open(path)
        exif_data = image.getexif()
        if exif_data is None or len(exif_data) == 0:
            print(f"No EXIF data found for {path}")
            return None

        date_fields = [36867, 36868, 306]  # DateTimeOriginal, DateTimeDigitized, DateTime
        for tag in date_fields:
            date_str = exif_data.get(tag)
            if date_str:
                try:
                    return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                except ValueError as e:
                    print(f"Error parsing EXIF date for {path}: {e}")

    except (UnidentifiedImageError, OSError) as e:
        print(f"Error opening image for EXIF extraction: {e}")
    
    return None

def extract_date_from_filename(filename):
    """Extract year and month from filenames in the format 'YYYYMM'."""
    # Regex to match filenames like 'PXL_20230701_181947815.TS' or 'IMG_20211212_120000.jpg'
    match = re.search(r'(\d{4})(\d{2})', filename)
    if match:
        year = match.group(1)
        month = match.group(2)
        if 1 <= int(month) <= 12:
            return datetime(year=int(year), month=int(month), day=1)
    return None

def get_file_creation_date(path):
    """Get the file system's creation date (fallback to modification date if unavailable)."""
    try:
        creation_time = os.path.getctime(path)
        return datetime.fromtimestamp(creation_time)
    except Exception as e:
        print(f"Error getting creation time for {path}: {e}")
        return datetime.fromtimestamp(os.path.getmtime(path))

def copy_file_if_not_exists(src, dst_folder):
    """Try to copy the file to the destination folder, skip if file already exists."""
    dst_file = os.path.join(dst_folder, os.path.basename(src))
    if os.path.exists(dst_file):
        print(f"File already exists, skipping: {os.path.basename(src)}")
        return
    shutil.copy(src, dst_file)
    print(f"Copied {os.path.basename(src)} to {dst_folder}")

def process_files(root, directory):
    """Process files in the directory and copy them to year/month folders in the root directory."""
    total_files_found = 0
    total_files_copied = 0
    total_files_unknown = 0

    month_names = ['01.January', '02.February', '03.March', '04.April', '05.May', '06.June',
                   '07.July', '08.August', '09.September', '10.October', '11.November', '12.December']

    for subdir, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(subdir, file)
            file_ext = os.path.splitext(file)[1].lower()

            if file_ext not in IMAGE_EXTENSIONS and file_ext not in VIDEO_EXTENSIONS:
                print(f"Skipping non-image/non-video file: {file}")
                continue

            total_files_found += 1
            date_taken = None

            if file_ext in IMAGE_EXTENSIONS:
                date_taken = get_image_exif_date(filepath)
            if not date_taken:
                date_taken = extract_date_from_filename(file)
            if not date_taken:
                date_taken = get_file_creation_date(filepath)

            if date_taken:
                year_folder = os.path.join(root, str(date_taken.year))
                month_folder = os.path.join(year_folder, month_names[date_taken.month - 1])

                if not os.path.exists(year_folder):
                    os.makedirs(year_folder)
                if not os.path.exists(month_folder):
                    os.makedirs(month_folder)

                copy_file_if_not_exists(filepath, month_folder)
                total_files_copied += 1
            else:
                unknown_folder = os.path.join(root, 'Unknown')
                if not os.path.exists(unknown_folder):
                    os.makedirs(unknown_folder)
                copy_file_if_not_exists(filepath, unknown_folder)
                total_files_unknown += 1

    return total_files_found, total_files_copied, total_files_unknown

def main():
    root = os.getcwd()

    while True:
        print("\nOptions:")
        print("0 - Quit")
        print("1 - Process all media files in all folders")
        print("2 - Select a specific folder to process")
        print("3 - Delete all JSON files")
        print("4 - Rename folders by month order")
        choice = input("Enter your choice: ")

        if choice == '0':
            break
        elif choice == '1':
            found, copied, unknown = process_files(root, root)
            print(f"Total files found: {found}, Total files copied: {copied}, Total files skipped (unknown): {unknown}")
        elif choice == '2':
            directories = list_directories(root)
            for i, directory in enumerate(directories):
                print(f"{i + 1} - {directory}")
            selected = int(input("Select a folder by number: ")) - 1
            if 0 <= selected < len(directories):
                found, copied, unknown = process_files(root, os.path.join(root, directories[selected]))
                print(f"Total files found: {found}, Total files copied: {copied}, Total files skipped (unknown): {unknown}")
        elif choice == '3':
            delete_json_files(root)
        elif choice == '4':
            rename_folders_by_month(root)

if __name__ == "__main__":
    main()
