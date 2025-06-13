const { Tray, Menu } = require('electron')
const { newtonFs }   = require('./fs');



const load = (win) => {
    let trayIcon = new Tray( newtonFs.getIconPath() );

    const trayMenuTemplate = [
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
            label: 'Settings',
            click: () => win.webContents.send('menu-actions', "open-settings")
        }, {
            label: 'Help',
            click: () => win.webContents.send('menu-actions', "show-about")
        }
    ];
     
    trayIcon.setContextMenu(
        Menu.buildFromTemplate(trayMenuTemplate)
    );
}


module.exports = {
    systemTray: {
        load: load,
    }
};