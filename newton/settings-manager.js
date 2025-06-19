const { newtonFs } = require('./fs');


let config = {};


const loadsettings = () => {
    config = JSON.parse(
        newtonFs.getSettingsConfigData()
    );
}

const getConfig = () => {
    return config;
}

const saveConfig = (window) => {
    if (!window) return;

    const windowBounds = window.getBounds();

    config["config"]["main_window_x"]      = windowBounds.x;
    config["config"]["main_window_y"]      = windowBounds.y;
    config["config"]["main_window_width"]  = windowBounds.width;
    config["config"]["main_window_height"] = windowBounds.height;

    newtonFs.saveSettingsConfigData(
        JSON.stringify(config, null, 4)
    );
}

const getIconPath = () => {
    return newtonFs.getIconPath();
}



module.exports = {
    settingsManager: {
        getIconPath: getIconPath,
        loadsettings: loadsettings,
        getConfig: getConfig,
        saveConfig: saveConfig,
    }
};