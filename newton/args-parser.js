const { app } = require('electron');


let startType   = "build";
let isDebug     = false;
let args        = [];



const loadKWArgs = () => {
    console.log("\n\nStart KWArgs:");

    const hasStartAs = app.commandLine.hasSwitch("start-as");
    if (hasStartAs) {
        startType = app.commandLine.getSwitchValue("start-as");
        console.log("Has start-as switch...");
        console.log(startType);
    }

    const hasDebug = app.commandLine.hasSwitch("app-debug");
    if (hasDebug) {
        isDebug = app.commandLine.getSwitchValue("app-debug");
        console.log("Has app-debug switch...");
        console.log(isDebug);
    }
}

const loadVArgs = () => {
    console.log("\n\nStart VArgs:");

    if (
        process.argv[0].endsWith("electron")
    ) {
        process.argv = process.argv.slice(2);
    }

    if (
        process.argv[0].endsWith("/newton") ||
        process.argv[0].endsWith(".AppImage")
    ) {
        process.argv = process.argv.slice(1);
    }

    if ( process.argv.length > 0 && (
        process.argv[0].includes("--trace-warnings") ||
        process.argv[0].includes("--start-as")
        )
    ) {
        process.argv = process.argv.slice(1);
    }

    if ( process.argv.length > 0 && (
        process.argv[0].includes("--trace-warnings") ||
        process.argv[0].includes("--start-as")
        )
    ) {
        process.argv = process.argv.slice(1);
    }

    args = process.argv;
    args.forEach((val, index, array) => {
        console.log(index + ': ' + val);
    }); 

    console.log("\n\n");
}

const loadArgs = () => {
    loadKWArgs();
    loadVArgs();
}


const getArgs = () => {
    return args;
}

const getStartType = () => {
    return startType;
}

const debugMode = () => {
    return isDebug;
}


module.exports = {
    argsParser: {
        loadArgs: loadArgs,
        getArgs: getArgs,
        getStartType: getStartType,
        debugMode: debugMode,
    }
};