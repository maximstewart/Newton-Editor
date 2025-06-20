const { dialog }     = require('electron');
const path           = require('node:path');
const fs             = require('node:fs');
const os             = require('os');
const chokidar       = require('chokidar');


const HOME_DIR                = os.homedir();
const BASE_PATH               = '../build/app';
const CONFIG_PATH             = path.join(HOME_DIR, "/.config/newton/");
const SETTINGS_CONFIG_PATH    = path.join(CONFIG_PATH, "/settings.json");
const LSP_CONFIG_PATH         = path.join(BASE_PATH, "/resources/lsp-servers-config.json");
let window                    = null;
let watcher                   = null;
let skipWatchChangeUpdateOnce = false;



const getIconPath = () => {
    return path.join(CONFIG_PATH, "./icons/newton.png");
}

const getSettingsConfigData = () => {
    return getFileContents(
        SETTINGS_CONFIG_PATH,
        useRelativePath = false,
        watchFile = false
    );
}

const getLspConfigData = () => {
    return getFileContents(
        LSP_CONFIG_PATH,
        useRelativePath = true,
        watchFile = false
    ).replaceAll("{user.home}", HOME_DIR);
}

const getFileContents = (_path, useRelativePath = false, watchFile = true) => {
    console.log(`Getting Contents For: ${_path}`);

    try {
        if (useRelativePath)
            return fs.readFileSync(
                path.join(__dirname, _path),
                'utf8'
            );

        if (watchFile)
            watcher.add(_path);

        return fs.readFileSync(_path, 'utf8');
    } catch(err) {
        return `{"message": {"type": "error", "text": "Error: Could not read  ${_path}"}}`;
    }
}

const setWindow = (win) => {
        window = win;
}

const saveSettingsConfigData = (data) => {
    saveFile(SETTINGS_CONFIG_PATH, data);
}

const saveFile = (fpath, content)  => {
    skipWatchChangeUpdateOnce = true;

    fs.writeFile(fpath, content, (err) => {
        if (err) {
            console.error("An error ocurred writing to the file " + err.message);
            return;
        }

        let parentDir = path.dirname(fpath);
        let watchers  = watcher.getWatched();
        let targetDir = watchers[parentDir];
        if (
            targetDir && !targetDir.includes( path.basename(fpath) )
        ) {
            skipWatchChangeUpdateOnce = false;
            watcher.add(fpath);
            window.webContents.send('update-file-path', fpath);
        }

        try {
            window.webContents.send('file-saved', fpath);
        } catch(e) {}
    });
}

const saveFileAs = (content) => {
    dialog.showSaveDialog().then((response) => {
        if (response.canceled) {
            console.debug("You didn't save the file");
            return;
        }

        saveFile(response.filePath, content);
    });
}

const openFiles = (startPath) => {
    dialog.showOpenDialog(
        {
            title: "Open File(s):",
            defaultPath: (startPath) ? startPath : HOME_DIR,
            filters: [
                { name: "All Files", extensions: ["*"]                               },
                { name: "All Sub Filters",
                    extensions: [
                        "h", "c", "hpp", "cpp", "js", "css", "scss", "html",
                        "ts", "java", "py", "pyc", "txt", "log", "md", "r",
                        "rc", "go"
                    ]
                },
                { name: "C",         extensions: ["h", "c"]                          },
                { name: "CPP",       extensions: ["hpp", "cpp"]                      },
                { name: "HTML",      extensions: ["js", "css", "scss", "html", "ts"] },
                { name: "Java",      extensions: ["java"]                            },
                { name: "Python",    extensions: ["py", "pyc"]                       },
                { name: "Text",      extensions: ["txt", "log", "md"]                },
                { name: "Rust",      extensions: ["r", "rc"]                         },
                { name: "Go",        extensions: ["go"]                              }
            ],
            properties: [
                'openFile',
                'multiSelections'
            ]
        }
    ).then((response) => {
        if (response.canceled) {
            console.debug("Canceled file(s) open request...");
            return;
        }

        window.webContents.send('load-files', response.filePaths);
        watcher.add(response.filePaths);
    });
}

const loadFilesWatcher = () => {
    watcher = chokidar.watch([], {});

    watcher.on('change', (fpath) => {
        if (skipWatchChangeUpdateOnce) {
            skipWatchChangeUpdateOnce = false;
            return;
        }

        console.debug("File (changed) : ", fpath);
        window.webContents.send('file-changed', fpath);
    }).on('unlink', (fpath) => {
        console.debug("File (deleted) : ", fpath);
        window.webContents.send('file-deleted', fpath);
    });
}

const unwatchFile = async (fpath) => {
    console.debug("File (unwatch) : ", fpath);
    await watcher.unwatch(fpath);
}

const closeFile = (fpath) => {
    unwatchFile(fpath);
}



module.exports = {
    newtonFs: {
        setWindow: setWindow,
        openFiles: openFiles,
        saveFile: saveFile,
        saveFileAs: saveFileAs,
        closeFile: closeFile,
        getIconPath: getIconPath,
        getFileContents: getFileContents,
        getLspConfigData: getLspConfigData,
        getSettingsConfigData: getSettingsConfigData,
        saveSettingsConfigData: saveSettingsConfigData,
        loadFilesWatcher: loadFilesWatcher,
        unwatchFile: unwatchFile,
    }
};