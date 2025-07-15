const { app } = require('electron');


let startType = "build";
let ipcPort   = "4563";
let isDebug   = false;
let args      = [];



const loadKWArgs = () => {
    console.log("\n\nStart KWArgs:");

    const hasStartAs = app.commandLine.hasSwitch("start-as");
    if (hasStartAs) {
        startType = app.commandLine.getSwitchValue("start-as");
        console.log("Has start-as switch...");
        console.log(startType);
    }

    const hasIpcPort = app.commandLine.hasSwitch("ipc-port");
    if (hasIpcPort) {
        ipcPort = app.commandLine.getSwitchValue("ipc-port");
        console.log("Has ipc-port switch...");
        console.log(ipcPort);
    }

    const hasDebug = app.commandLine.hasSwitch("app-debug");
    if (hasDebug) {
        isDebug = app.commandLine.getSwitchValue("app-debug");
        console.log("Has app-debug switch...");
        console.log(isDebug);
    }
}

const filterOutLaunchAndKWArgs = () => {
    if (
        process.argv[0].endsWith("electron")
    ) {
        process.argv = process.argv.slice(2);
    }

    do {
        process.argv = process.argv.slice(1);
    } while (
        process.argv.length > 0 &&
        (
            process.argv[0].endsWith("/newton") ||
            process.argv[0].endsWith(".AppImage") ||
            process.argv[0].includes("--trace-warnings") ||
            process.argv[0].includes("--start-as") ||
            process.argv[0].includes("--ipc-port")
        )
    );
}

const loadVArgs = () => {
    console.log("\n\nStart VArgs:");
    args = process.argv;
    args.forEach((val, index, array) => {
        console.log(index + ': ' + val);
    }); 

    console.log("\n\n");
}

const loadArgs = () => {
    loadKWArgs();
    filterOutLaunchAndKWArgs();
    loadVArgs();
}


const getArgs = () => {
    return args;
}

const getStartType = () => {
    return startType;
}

const getDebugMode = () => {
    return isDebug;
}

const getIpcPort = () => {
    return ipcPort;
}


module.exports = {
    argsParser: {
        loadArgs: loadArgs,
        getArgs: getArgs,
        getStartType: getStartType,
        getDebugMode: getDebugMode,
        getIpcPort: getIpcPort,
    }
};