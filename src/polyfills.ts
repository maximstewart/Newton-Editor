/**
 * This file includes polyfills needed by Angular and is loaded before the app.
 * You can add your own extra polyfills to this file.
 */

/***************************************************************************************************
 * Zone JS is required by Angular itself.
 */


import 'zone.js';  // Included with Angular CLI.


// Note: Is set to 'any' b/c of desire to set 'render'
// side if running outside of electron mode.
declare global {
    interface Window {
        electron: {
            node: any,
            chrome: any,
            electron: any,
        },
        main: {
            onMenuActions: any,
            onTerminalActions: any,
            quit: any,
            toggleFullScreen: any,
        },
        fs: {
            getLspConfigData: any,
            getFileContents: any,
            openFiles: any,
            saveFile: any,
            saveFileAs: any,
            chooseFolder: any,
            closeFile: any,
            getPathForFile: any,
            onLoadFiles: any,
            onUpdateFilePath: any,
            onSavedFile: any,
            onChangedFile: any,
            onDeletedFile: any,
        }
    }
}