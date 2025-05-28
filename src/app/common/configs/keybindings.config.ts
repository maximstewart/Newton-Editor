export const Keybindings: Array<any> = [
// export const Keybindings: any = [
    // {
    //     name: "showSettingsMenu",
    //     bindKey: {win: "Ctrl-Shift-m", mac: "Ctrl-Shift-m"},
    //     exec: () => {
    //         ace.config.loadModule("ace/ext/settings_menu", function(module) {
    //             module.init(editor);
    //             editor.showSettingsMenu();
    //         })
    //     }
    // }, {
    //     name: "showKeyboardShortcuts",
    //     bindKey: {win: "ctrl-shift-h", mac: "command-shift-h"},
    //     exec: () => {
    //         ace.config.loadModule("ace/ext/keybinding_menu", function(module) {
    //             module.init(editor);
    //             editor.showKeyboardShortcuts();
    //         })
    //     }
    // }, {
    //     name: "openCommandPalette2",
    //     bindKey: {linux: "Command-Shift-/|F1", win: "Ctrl-Shift-/|F1"},
    //     exec: () => {
    //         editor.execCommand("openCommandPalette");
    //     }
    // }, {
    //     name: "showLSPManager",
    //     bindKey: {win: "ctrl-m", mac: "command-m"},
    //     exec: () => {
    //         $('//lsp-modal').modal("toggle");
    //     }
    // }, {
     {
         name: "search",
         bindKey: {win: "ctrl-f", mac: "ctrl-f"},
         exec: () => {
             // blockHigherNewtonEvePropigation = true;
             // searchReplace.toggleShow();
            console.log("Search");
         },
         readOnly: true
     }
    // }, {
    //     name: "openFile",
    //     bindKey: {win: "ctrl-o", mac: "ctrl-o"},
    //     exec: () => {
    //         fpath = aceSessions[currentSession]["fpath"]
    //         sendMessage("open_file", "", "", fpath, "");
    //     },
    //     readOnly: true
    // }, {
    //     name: "saveSession",
    //     bindKey: {win: "ctrl-s", mac: "ctrl-s"},
    //     exec: () => {
    //         saveSession(currentSession);
    //     },
    //     readOnly: true
    // }, {
    //     name: "newSession",
    //     bindKey: {win: "ctrl-t", mac: "ctrl-t"},
    //     exec: () => {
    //         newSession();
    //     },
    //     readOnly: true
    // }, {
    //     name: "closeSession",
    //     bindKey: {win: "ctrl-w", mac: "ctrl-w"},
    //     exec: () => {
    //         closeSession(currentSession);
    //     },
    //     readOnly: true
    // }, {
    //     name: "toggleLineHighlight",
    //     bindKey: {win: "ctrl-h", mac: "ctrl-h"},
    //     exec: () => {
    //         toggleLineHighlight();
    //     },
    //     readOnly: true
    // }, {
    //     name: "gotoDefinition",
    //     bindKey: {win: "ctrl-g", mac: "ctrl-g"},
    //     exec: () => {
    //         console.log("Goto stub...");
    //          lspProvider.$messageController.postMessage(Message(), callback);
    //     },
    //     readOnly: true
    // }, {
    //     name: "movelinesUp",
    //     bindKey: {win: "ctrl-up", mac: "ctrl-up"},
    //     exec: () => {
    //         editor.execCommand("movelinesup");
    //     },
    //     readOnly: true
    // }, {
    //     name: "movelinesDown",
    //     bindKey: {win: "ctrl-down", mac: "ctrl-down"},
    //     exec: () => {
    //         editor.execCommand("movelinesdown");
    //     },
    //     readOnly: true
    // }, {
    //     name: "tgglTopMainMenubar",
    //     bindKey: {win: "ctrl-0", mac: "ctrl-0"},
    //     exec: () => {
    //         sendMessage("tggl_top_main_menubar", "", "", "", "");
    //     },
    //     readOnly: true
    // }, {
    //     name: "zoomIn",
    //     bindKey: {win: "ctrl-=", mac: "ctrl-="},
    //     exec: () => {
    //         zoomIn();
    //     },
    //     readOnly: true
    // }, {
    //     name: "zoomOut",
    //     bindKey: {win: "ctrl--", mac: "ctrl--"},
    //     exec: () => {
    //         zoomOut();
    //     },
    //     readOnly: true
    // }, {
    //     name: "scrollUp",
    //     bindKey: {win: "alt-up", mac: "alt-up"},
    //     exec: () => {
    //         editor.execCommand("scrollup");
    //     },
    //     readOnly: true
    // }, {
    //     name: "scrollDown",
    //     bindKey: {win: "alt-down", mac: "alt-down"},
    //     exec: () => {
    //         editor.execCommand("scrolldown");
    //     },
    //     readOnly: true
    // }, {
    //     name: "launhLSP",
    //     bindKey: {win: "ctrl-l", mac: "ctrl-l"},
    //     exec: () => {
    //         loadLSPManager();
    //     },
    //     readOnly: true
    // }

];