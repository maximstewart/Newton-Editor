/**
 * This file includes polyfills needed by Angular and is loaded before the app.
 * You can add your own extra polyfills to this file.
 */

/***************************************************************************************************
 * Zone JS is required by Angular itself.
 */


import 'zone.js';  // Included with Angular CLI.


declare global {
    interface Window {
        electron: {
            node: () => Promise<string>,
            chrome: () => Promise<string>,
            electron: () => Promise<string>,
        },
        main: {
            onMenuActions: (arg0: any) => Promise<string>,
            quit: any,
            toggleFullScreen: any,
        },
        fs: {
            getLspConfigData: () => Promise<string>,
            getFileContents: (arg0: any) => Promise<string>,
            openFiles: (arg0) => Promise<string>,
            saveFile: (arg0: any, arg1: any) => Promise<string>,
            saveFileAs: () => Promise<string>,
            chooseFolder: () => Promise<string>,
            closeFile: (arg0: any) => Promise<string>,
            getPathForFile: any,
            onLoadFiles: (arg0: any) => Promise<string>,
            onUpdateFilePath: (arg0: any) => Promise<string>,
            onSavedFile: (arg0: any) => Promise<string>,
            onChangedFile: (arg0: any) => Promise<string>,
            onDeletedFile: (arg0: any) => Promise<string>,
        }
    }
}