import os

INPUT_DIRECTORY = "./app"
OUTPUT_DIRECTORY = "./build"

os.makedirs(OUTPUT_DIRECTORY, mode=777, exist_ok=True)

def getUpdatedContent(file_path, content):
    if file_path.__contains__("main.py"):
        semiUpdatedContent = content.replace('# Store.configSpace(self.storeIndex) This line is commented because unpredictible errors while testing', 'Store.configSpace(self.storeIndex)')
        semiUpdatedContent = semiUpdatedContent.replace('# Store.configCategory(self.storeIndex) This line is commented because unpredictible errors while testing', 'Store.configCategory(self.storeIndex)')
        semiUpdatedContent = semiUpdatedContent.replace('# Store.stopConfigCategory(self.storeIndex) This line is commented because unpredictible errors while testing', 'Store.stopConfigCategory(self.storeIndex)')
        semiUpdatedContent = semiUpdatedContent.replace('# getMongoInfo() This line was commented so it does not load categories or stores that could change the tests', 'getMongoInfo()')
        semiUpdatedContent = semiUpdatedContent.replace('# sys.exit(app.exec_()) This line is commented, so the tests can run correctly', 'sys.exit(app.exec_())')
        semiUpdatedContent = semiUpdatedContent.replace('# Mongo.closeMongoConnection() This line is commented, so mongodb connections can work properly while testing', 'Mongo.closeMongoConnection()')
        semiUpdatedContent = semiUpdatedContent.replace('app.', '')
        return semiUpdatedContent.replace('sys.exit(exec_())', 'sys.exit(app.exec_())')
    else:
        return content.replace('app.', '')

def updateFiles(files):
    for file in files:
        file_path = os.path.join(root, file)  # Full path to the file

        if not file_path.__contains__("__init__") and not root.__contains__("__pycache__"):
            try:
                # Read files
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
    
                resultDirectory = file_path.replace(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
                updatedContent = getUpdatedContent(file_path, content)

                os.makedirs(resultDirectory, mode=777, exist_ok=True)

                # Write files
                with open(resultDirectory, 'w', encoding='utf-8') as newFile:
                    newFile.write(updatedContent)

                print(f"Updated file: {resultDirectory}")
            except Exception as e:
                print(f"Skipped {file_path} file due to error: {e}")
        else:
            print(f"Skipped {file_path} file due to unnecesary changes needed")

# Walk through all files in the folder (and subfolders if any)
for root, dirs, files in os.walk(INPUT_DIRECTORY):
    if not root.__contains__("__init__") and not root.__contains__("__pycache__"):
        updateFiles(files)
    else:
        print(f"Skipped {root} directory due to unnecesary changes needed")
