import os
import shutil
from datetime import datetime
from PIL import Image, UnidentifiedImageError
import win32com.client
from dateutil import parser  # Dynamic date parser to handle varying date formats
import re  # For cleaning up non-ASCII characters from strings

# Define image and video extensions separately
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv']

def list_directories(path):
    """List all directories at a given path."""
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def get_image_exif_date(path):
    """Attempt to get the 'Date Taken' from image EXIF data."""
    try:
        image = Image.open(path)
        
        # Check if the image supports EXIF data (GIF, for example, does not)
        if image.format == 'GIF':  # GIFs do not have EXIF data
            print(f"GIF format detected, skipping EXIF extraction for {path}")
            return None

        # Use getexif() instead of _getexif() for newer versions of Pillow
        exif_data = image.getexif()
        if exif_data:
            # Standard EXIF tag for 'Date Taken'
            date_taken = exif_data.get(36867)
            if date_taken:
                return datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
    except (UnidentifiedImageError, OSError, AttributeError) as e:
        print(f"Error reading EXIF for {path}: {e}")
    return None

def clean_date_string(date_str):
    """Remove non-printable and non-ASCII characters from the date string."""
    # Use a regex to remove non-ASCII characters
    clean_str = re.sub(r'[^\x00-\x7F]+', '', date_str)
    return clean_str.strip()

def get_windows_date_taken(path):
    """Get the 'Date Taken' property from file properties in Windows."""
    try:
        shell = win32com.client.Dispatch("Shell.Application")
        folder = shell.Namespace(os.path.dirname(path))
        file = folder.ParseName(os.path.basename(path))
        date_taken = folder.GetDetailsOf(file, 12)  # 12 corresponds to 'Date Taken' in Windows
        
        # Check if 'Date Taken' is found and try to parse it
        if date_taken:
            try:
                # Clean the date string to remove unwanted characters
                cleaned_date = clean_date_string(date_taken)
                # Use dateutil.parser to handle multiple formats dynamically
                parsed_date = parser.parse(cleaned_date)  # Normalize and parse
                return parsed_date
            except Exception as e:
                print(f"Error parsing 'Date Taken' format: {cleaned_date}. Error: {e}")
    except Exception as e:
        print(f"Error accessing 'Date Taken' from Windows properties for {path}: {e}")
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

    for subdir, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(subdir, file)
            file_ext = os.path.splitext(file)[1].lower()

            # Skip any file that is not an image or a video
            if file_ext not in IMAGE_EXTENSIONS and file_ext not in VIDEO_EXTENSIONS:
                print(f"Skipping non-image/non-video file: {file}")
                continue

            total_files_found += 1
            date_taken = None

            # Use EXIF for images, skip EXIF for videos
            if file_ext in IMAGE_EXTENSIONS:
                date_taken = get_image_exif_date(filepath)
                if not date_taken:
                    print(f"No EXIF data found for {file}, trying to get 'Date Taken' from Windows properties.")
                    date_taken = get_windows_date_taken(filepath)  # Get 'Date Taken' from Windows
                if not date_taken:
                    print(f"No 'Date Taken' data from Windows properties, using file creation date.")
                    date_taken = get_file_creation_date(filepath)
            elif file_ext in VIDEO_EXTENSIONS:
                print(f"Video file detected: {file}, using file creation date.")
                date_taken = get_file_creation_date(filepath)

            # Handle files with no valid date
            if date_taken:
                # Create year/month folder based on the date
                year_folder = os.path.join(root, str(date_taken.year))
                month_folder = os.path.join(year_folder, date_taken.strftime('%B'))

                if not os.path.exists(year_folder):
                    os.makedirs(year_folder)
                if not os.path.exists(month_folder):
                    os.makedirs(month_folder)

                # Try to copy the file if it doesn't exist at the destination
                copy_file_if_not_exists(filepath, month_folder)
                total_files_copied += 1
            else:
                print(f"Could not determine date for {file}, skipping.")
                total_files_unknown += 1

    return total_files_found, total_files_copied, total_files_unknown

def delete_json_files(directory):
    """Delete all JSON files within the directory."""
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                os.remove(os.path.join(subdir, file))
                print(f"Deleted {file}")

def main():
    root = os.getcwd()

    while True:
        print("\nOptions:")
        print("0 - Quit")
        print("1 - Process all media files in all folders")
        print("2 - Select a specific folder to process")
        print("3 - Delete all JSON files")
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

if __name__ == "__main__":
    main()
