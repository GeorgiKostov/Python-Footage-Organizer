import os
import shutil

# Define source and destination directories based on the script's location
script_directory = os.path.dirname(os.path.realpath(__file__))
source_directory = os.path.join(script_directory, "gameboyroms")
destination_directory = os.path.join(script_directory, "gbcselection")

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

def find_and_copy_files():
    while True:
        game_name = input("Enter a game name (or 0 to quit): ")
        if game_name == "0":
            print("Exiting program.")
            break

        matched_files = []

        # Recursively search for matching files in the source directory and subfolders
        for root, dirs, files in os.walk(source_directory):
            for filename in files:
                if filename.lower().endswith('.gbc') and game_name.lower() in filename.lower():
                    matched_files.append(os.path.join(root, filename))
        
        if not matched_files:
            print(f"No files found for: {game_name}")
        else:
            print(f"\nFound files for: {game_name}")
            for i, file in enumerate(matched_files, start=1):
                print(f"{i}. {os.path.basename(file)}")
            
            while True:
                choice = input("Enter the numbers of the files to copy (separated by commas), or 0 to finish with this game: ")
                if choice == "0":
                    print("No more files will be selected for this game.")
                    break
                try:
                    choices = map(int, choice.split(','))
                    for choice in choices:
                        if 1 <= choice <= len(matched_files):
                            source_file_path = matched_files[choice - 1]
                            destination_file_path = os.path.join(destination_directory, os.path.basename(source_file_path))
                            shutil.copy(source_file_path, destination_file_path)
                            print(f"Copied: {os.path.basename(source_file_path)} to {destination_directory}")
                        else:
                            print("Invalid number: {}, please try again.".format(choice))
                except ValueError:
                    print("Invalid input, make sure to enter only numbers separated by commas.")

if __name__ == "__main__":
    find_and_copy_files()
