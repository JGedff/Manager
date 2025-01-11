import shutil
import os

DIRECTORY = "app_tests"
OUTPUT_DIR = "app"

textToReplace = "app_tests."
newText = ""

print(f"Source directory: \033[92m{DIRECTORY}\033[0m")
print(f"Output directory: \033[92m{OUTPUT_DIR}\033[0m")
print("")

# Remove output folder if exists
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
    print(f"\033[91mFolder {OUTPUT_DIR} deleted\033[0m")

# Copy the folder
shutil.copytree(DIRECTORY, OUTPUT_DIR)
print("\033[92mFolder copied successfully\033[0m")
print("")

def replaceFile(path, searchString, replaceString):
    updated_content = ""

    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    if "main.py" in path:
        updated_content = content.replace(searchString, replaceString)
        updated_content = updated_content.replace("# sys.exit(app.exec_()) This line is commented, so the tests can run correctly", "sys.exit(app.exec_())")
        updated_content = updated_content.replace("# getMongoInfo() This line was commented so it does not load categories or stores that could change the tests", "getMongoInfo()")
        updated_content = updated_content.replace("# Store.configSpace(self.storeIndex) This line is commented because unpredictible errors while testing", "Store.configSpace(self.storeIndex)")
        updated_content = updated_content.replace("# Mongo.closeMongoConnection() This line is commented, so mongodb connections can work properly while testing", "Mongo.closeMongoConnection()")
        updated_content = updated_content.replace("# Store.configCategory(self.storeIndex) This line is commented because unpredictible errors while testing", "Store.configCategory(self.storeIndex)")
        updated_content = updated_content.replace("# Store.stopConfigCategory(self.storeIndex) This line is commented because unpredictible errors while testing", "Store.stopConfigCategory(self.storeIndex)")
    else:
        updated_content = content.replace(searchString, replaceString)

    # Write back the updated content to the file
    with open(path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    print(f"Updated: {path}")

def replaceDirectory(folder, searchString, replaceString):
    for root, _, files in os.walk(folder):
        if not "__" in root:
            for file in files:
                filepath = os.path.join(root, file)

                if not "__" in file:
                    replaceFile(filepath, searchString, replaceString)
                else:
                    print(f"\033[93mSkipped file: {filepath} due to not needed changes\033[0m")

                    try:
                        os.remove(filepath)

                        print(f"\033[91mRemoved file:\033[0m {filepath} \033[91mdue to be unnecessary\033[0m")
                    except:
                        pass
        else:
            print(f"\033[93mSkipped folder: {root} due to not needed changes\033[0m")

            try:
                os.remove(root)

                print(f"\033[91mRemoved folder:\033[0m {root} \033[91mdue to be unnecessary\033[0m")
            except:
                pass

# Replace
replaceDirectory(OUTPUT_DIR, textToReplace, newText)
print("")
print("\033[92mReplacement completed\033[0m")
