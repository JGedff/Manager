const { existsSync, mkdirSync, lstatSync, readFileSync, readdirSync, rmSync, writeFileSync } = require("node:fs")
const join = require('node:path').join

const getUpdatedContent = (file_path = '', content = '') => {
    if (file_path.includes("main.py")) {
        let semiUpdatedContent = content.replace('# Store.configSpace(self.storeIndex) This line is commented because unpredictible errors while testing', 'Store.configSpace(self.storeIndex)')
        semiUpdatedContent = semiUpdatedContent.replace('# Store.configCategory(self.storeIndex) This line is commented because unpredictible errors while testing', 'Store.configCategory(self.storeIndex)')
        semiUpdatedContent = semiUpdatedContent.replace('# Store.stopConfigCategory(self.storeIndex) This line is commented because unpredictible errors while testing', 'Store.stopConfigCategory(self.storeIndex)')
        semiUpdatedContent = semiUpdatedContent.replace('# getMongoInfo() This line was commented so it does not load categories or stores that could change the tests', 'getMongoInfo()')
        semiUpdatedContent = semiUpdatedContent.replace('# sys.exit(app.exec_()) This line is commented, so the tests can run correctly', 'sys.exit(app.exec_())')
        semiUpdatedContent = semiUpdatedContent.replace('# Mongo.closeMongoConnection() This line is commented, so mongodb connections can work properly while testing', 'Mongo.closeMongoConnection()')
        semiUpdatedContent = semiUpdatedContent.replaceAll('app.', '')
        return semiUpdatedContent.replace('sys.exit(exec_())', 'sys.exit(app.exec_())')
    }
    else {
        return content.replace('app.', '')
    }
}

const modifyContent = (file_path = '') => {
    if (!file_path.includes("__")) {
        try {
            // Read files
            let content = readFileSync(file_path, { encoding: 'utf-8' })

            let resultDirectory = file_path.replace(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
            let updatedContent = getUpdatedContent(file_path, content)

            // Write files
            writeFileSync(resultDirectory, updatedContent, { encoding: 'utf-8' })

            console.log(`Updated file: ${resultDirectory}`)
        }
        catch (e) {
            console.error(`Skipped ${file_path} file due to error: ${e}`)
        }
    }
    else {
        console.warn(`Skipped ${file_path} due to not needed changes`)
    }
}

const updateFiles = (path = '' || [''], root = '') => {
    if (!path.includes("__") && !root.includes("__")) {
        if (lstatSync(`${root}/${path}`).isDirectory()) {
            let files = readdirSync(`${root}/${path}`)

            outputRoot = root.replace('app', 'build')

            mkdirSync(`${outputRoot}/${path}`, true)

            files.forEach(file => {
                updateFiles(file, `${root}/${path}`)
            })
        }
        else {
            modifyContent(`${root}/${path}`)
        }
    }
    else {
        console.warn(`Skipped ${path} due to not needed changes`)
    }
}

const INPUT_DIRECTORY = join(__dirname, "/app")
const OUTPUT_DIRECTORY = join(__dirname, "/build")

let directory = readdirSync(INPUT_DIRECTORY)

if (existsSync(OUTPUT_DIRECTORY)) {
    rmSync(OUTPUT_DIRECTORY, { recursive: true, force: true })
}

mkdirSync(OUTPUT_DIRECTORY, true)

// Walk through all files in the folder (and subfolders if any)
directory.forEach(folder => {
    if (folder.includes("__")) {
        console.warn(`Skipped ${folder} due to not needed changes`)
    }
    else {
        updateFiles(folder, INPUT_DIRECTORY)
    }
})
