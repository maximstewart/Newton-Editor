const { Menu } = require('electron');



const load = (win) => {
    const menu = Menu.buildFromTemplate([
        {
            label: "File",
            submenu: [
                {
                    label: 'New',
                    click: () => win.webContents.send('menu-actions', "new-file")
                }, {
                    label: 'Open',
                    click: () => win.webContents.send('menu-actions', "open-files")
                }, {
                    label: 'save',
                    click: () => win.webContents.send('menu-actions', "save-file")
                }, {
                    label: 'Save As',
                    click: () => win.webContents.send('menu-actions', "save-file-as")
                }, {
                    label: 'Terminal',
                    click: () => {}
                }
            ]
        }, {
            label: "Edit",
            submenu: [
                {
                    label: 'Undo',
                    click: () => win.webContents.send('menu-actions', "undo")
                }, {
                    label: 'Redo',
                    click: () => win.webContents.send('menu-actions', "redo")
                }, {
                    label: 'Cut',
                    click: () => win.webContents.send('menu-actions', "cut")
                }, {
                    label: 'Copy',
                    click: () => win.webContents.send('menu-actions', "copy")
                }, {
                    label: 'Paste',
                    click: () => win.webContents.send('menu-actions', "paste")

                }, {
                    label: 'Delete',
                    click: () => win.webContents.send('menu-actions', "delete")
                }, {
                    label: 'Select All',
                    click: () => win.webContents.send('menu-actions', "select-all")
                }, {
                    label: 'Indent',
                    click: () => win.webContents.send('menu-actions', "blockindent")
                }, {
                    label: 'De-Indent',
                    click: () => win.webContents.send('menu-actions', "blockoutdent")
                }, {
                    label: 'To Upper Case',
                    click: () => win.webContents.send('menu-actions', "touppercase")
                }, {
                    label: 'To Lower Case',
                    click: () => win.webContents.send('menu-actions', "tolowercase")
                },
            ]
        }, {
            label: "View",
            submenu: [
                {
                    label: 'Zoom In',
                    click: () => win.webContents.send('menu-actions', "zoom-in")
                }, {
                    label: 'Zoom Out',
                    click: () => win.webContents.send('menu-actions', "zoom-out")
                }, {
                    label: 'Toggle Full Screen',
                    click: () => { win.setFullScreen(!win.fullScreen) }
                }, {
                    label: 'Toggle Developer Tools',
                    click: () => win.webContents.toggleDevTools()
                }
            ]
        }, {
            label: "Help",
            submenu: [
                {
                    label: 'About',
                    click: () => win.webContents.send('menu-actions', "show-about")
                }
            ]
        },

    ]);

    Menu.setApplicationMenu(menu)
}



module.exports = {
    menu: {
        load: load
    }
};