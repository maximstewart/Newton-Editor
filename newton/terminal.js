
const { ipcMain } = require('electron');
// const pty         = require('node-pty');
const os          = require("os");


const shell = "win32" === os.platform() ? "powershell.exe" : "bash";


const load = (win) => {
    // const ptyProcess = pty.spawn(shell, [], {
    //     name: "xterm-color",
    //     cols: 172,
    //     rows: 256,
    //     cwd: process.env.HOME,
    //     env: process.env
    // });
    
    // ptyProcess.on('data', function(data) {
    //     win.webContents.send("terminal-actions", data);
    // });

    // ipcMain.on("terminal-keystroke", (event, key) => {
    //     ptyProcess.write(key);
    // });

}
    
module.exports = {
    terminal: {
        load: load
    }
};


