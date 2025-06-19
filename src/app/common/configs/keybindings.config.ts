export const Keybindings: Array<{}> = [
    {
        name: "quit",
        bindKey: {win: "Ctrl-q", mac: "Ctrl-q"},
        readOnly: false
    }, {
        name: "toggleFullScreen",
        bindKey: {win: "F11", mac: "F11"},
        readOnly: false
    }, {
        name: "showSettingsMenu",
        bindKey: {win: "Ctrl-Shift-m", mac: "Ctrl-Shift-m"},
        readOnly: false
    }, {
        name: "showKeyboardShortcuts",
        bindKey: {win: "ctrl-shift-k", mac: "command-shift-k"},
        readOnly: false
    }, {
        name: "openCommandPalette",
        bindKey: {linux: "Command-shift-/|F1", win: "ctrl-shift-/|F1"},
        readOnly: false
    }, {
        name: "showFilesModal",
        bindKey: {win: "ctrl-b", mac: "ctrl-b"},
        service: "filesModalService",
        readOnly: false
    }, {
        name: "showLSPModal",
        bindKey: {win: "ctrl-shift-l", mac: "ctrl-shift-l"},
        readOnly: false
    }, {
        name: "search",
        bindKey: {win: "ctrl-f", mac: "ctrl-f"},
        readOnly: true
    }, {
        name: "newSession",
        bindKey: {win: "ctrl-t", mac: "ctrl-t"},
        readOnly: true
    }, {
        name: "destroySession",
        bindKey: {win: "ctrl-w", mac: "ctrl-w"},
        readOnly: false
    }, {
        name: "openFiles",
        bindKey: {win: "ctrl-o", mac: "ctrl-o"},
        readOnly: false
    }, {
        name: "saveFile",
        bindKey: {win: "ctrl-s", mac: "ctrl-s"},
        readOnly: false
    }, {
        name: "saveFileAs",
        bindKey: {win: "ctrl-shift-s", mac: "ctrl-shift-s"},
        readOnly: false
    }, {
        name: "selectLeftEditor",
        bindKey: {win: "ctrl-pageup", mac: "ctrl-pageup"},
        readOnly: false
    }, {
        name: "selectRightEditor",
        bindKey: {win: "ctrl-pagedown", mac: "ctrl-pagedown"},
        readOnly: false
    }, {
        name: "moveSessionLeft",
        bindKey: {win: "ctrl-shift-up", mac: "ctrl-shift-up"},
        readOnly: false
    }, {
        name: "moveSessionRight",
        bindKey: {win: "ctrl-shift-down", mac: "ctrl-shift-down"},
        readOnly: false
    }, {
        name: "cutToBuffer",
        bindKey: {win: "ctrl-k", mac: "ctrl-k"},
        readOnly: false
    }, {
        name: "pasteCutBuffer",
        bindKey: {win: "ctrl-u", mac: "ctrl-u"},
        readOnly: false
     }, {
        name: "movelinesUp",
        bindKey: {win: "ctrl-up", mac: "ctrl-up"},
        readOnly: false
     }, {
        name: "movelinesDown",
        bindKey: {win: "ctrl-down", mac: "ctrl-down"},
        readOnly: false
     }, {
        name: "duplicateLines",
        bindKey: {win: "ctrl-d", mac: "ctrl-d"},
        readOnly: false
     }, {
        name: "zoomIn",
        bindKey: {win: "ctrl-=", mac: "ctrl-="},
        readOnly: true
    }, {
        name: "zoomOut",
        bindKey: {win: "ctrl--", mac: "ctrl--"},
        readOnly: true
    }, {
        name: "toggleLineHighlight",
        bindKey: {win: "ctrl-h", mac: "ctrl-h"},
        readOnly: true
    }, {
        name: "gotoDefinition",
        bindKey: {win: "ctrl-g", mac: "ctrl-g"},
        readOnly: true
    }
];