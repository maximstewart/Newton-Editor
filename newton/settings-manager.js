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

const saveConfig = () => {
    console.log(config);
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
