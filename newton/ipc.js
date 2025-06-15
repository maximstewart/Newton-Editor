const express    = require('express');
const bodyParser = require('body-parser');
const http       = require('http');
const socketIO   = require('socket.io');
const fetch      = require('electron-fetch').default


const IPC_SERVER_IP         = "127.0.0.1";
let window                  = null;
let ipcServer               = null;
let ipcServerPort           = "4563";
let ipcServerURL            = `http://${IPC_SERVER_IP}:${ipcServerPort}`;


const setWindow = (win) => {
        window = win;
}

const loadIPCServer = (fpath) => {

    const app = express();
    ipcServer = http.createServer(app);
    const io  = socketIO(ipcServer);

    app.use(bodyParser.json());
    app.use(
        bodyParser.urlencoded({
            extended: true,
        }),
    );

    app.get("/is-up", (req, res) => {
        res.status(200).send('yes');
    });

    app.post("/load-files", (req, res) => {
        console.debug("Load File(s) : ", req.body);

        window.webContents.send('load-files', req.body);
        res.status(200).send('');
    });

    ipcServer.listen(ipcServerPort, () => {
        console.debug("IPCServer (start) : Started on port ", ipcServerPort, " .");
    });

}

const isIPCServerUp = async () => {
    const response = await fetch(`${ipcServerURL}/is-up`).catch((err) => {
        console.debug("IPCServer (status) : Not up; okay to start.");
        return {
            text: () => {
                return "no";
            }
        }
    });

    const body = await response.text();
    return (body == "yes") ? true : false;
}

const sendFilesToIPC = async (files) => {
    let request = {
        method: "POST",
        body: JSON.stringify(files),
        headers: { 'Content-Type': 'application/json' }
    };

    await fetch(`${ipcServerURL}/load-files`, request);
}


module.exports = {
    newtonIPC: {
        setWindow: setWindow,
        loadIPCServer: loadIPCServer,
        isIPCServerUp: isIPCServerUp,
        sendFilesToIPC: sendFilesToIPC,
    }
};