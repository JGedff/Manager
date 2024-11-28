import shutil
import os

DIRECTORY = "app_tests"
OUTPUT_DIR = "app"

textToReplace = "app_tests."
newText = "app."

print(f"Source directory: {DIRECTORY}")
print(f"Output directory: {OUTPUT_DIR}")

# Remove output folder if exists
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)

# Copy the folder
shutil.copytree(DIRECTORY, OUTPUT_DIR)
print("Folder copied successfully")

def replaceFile(path, searchString, replaceString):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    updated_content = content.replace(searchString, replaceString)

    # Write back the updated content to the file
    with open(path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    print(f"Updated: {path}")

def replaceDirectory(folder, searchString, replaceString):
    for root, _, files in os.walk(folder):
        if not "__" in root:
            for file in files:
                if not "__" in file:
                    filepath = os.path.join(root, file)
                    replaceFile(filepath, searchString, replaceString)
                else:
                    print(f"Skipped file: {file} due to no changes needed")
        else:
            print(f"Skipped folder: {root} due to no changes needed")


# Replace
replaceDirectory(OUTPUT_DIR, textToReplace, newText)
print("Replacement completed.")
