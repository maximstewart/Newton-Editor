import { Component } from "@angular/core";

// Import Ace and its modes/themes so that `ace` global is defined
import * as ace from "ace-builds/src-noconflict/ace";
import "ace-builds/src-noconflict/theme-one_dark";
import "ace-builds/src-noconflict/theme-dracula";
import "ace-builds/src-noconflict/ext-language_tools";

import { InfoBarService } from '../../common/services/editor/info-bar/info-bar.service';
import { EditorsService } from '../../common/services/editor/editors.service';
import { LSPService } from '../../common/services/lsp.service';

import { AceEditorBase } from './ace-editor.base';



@Component({
    selector: 'ace-editor',
    standalone: true,
    imports: [
    ],
    templateUrl: './ace-editor.component.html',
    styleUrl: './ace-editor.component.css',
    host: {
        'class': 'col'
    }
})
export class AceEditorComponent extends AceEditorBase {


    constructor(
        private infoBarService: InfoBarService,
        private editorsService: EditorsService,
        private lspService: LSPService
    ) {
        super();
    }


    public ngAfterViewInit(): void {
        if (this.isDefault) {
            this.addActiveStyling();
        }

        this.loadAce();
    }

    public loadAce(): void {
        ace.config.set('basePath', this.editorSettings.BASE_PATH);

        this.editor = ace.edit( this.editorElm.nativeElement );
        this.editor.setOptions( this.editorSettings.CONFIG );
        // this.editor.commands.addCommands( this.editorSettings.KEYBINDINGS );
        this.editor.commands.addCommands([
             {
                 name: "search",
                 bindKey: {win: "ctrl-f", mac: "ctrl-f"},
                 exec: () => {
                     this.search();
                 },
                 readOnly: true
             }, {
                 name: "movelinesUp",
                 bindKey: {win: "ctrl-up", mac: "ctrl-up"},
                 exec: () => {
                     this.movelinesUp();
                 },
                 readOnly: false
             }, {
                 name: "movelinesDown",
                 bindKey: {win: "ctrl-down", mac: "ctrl-down"},
                 exec: () => {
                     this.movelinesDown();
                 },
                 readOnly: false
             },
             {
                 name: "duplicateLines",
                 bindKey: {win: "ctrl-d", mac: "ctrl-d"},
                 exec: () => {
                     this.duplicateLines();
                 },
                 readOnly: false
             }, {
                 name: "zoomIn",
                 bindKey: {win: "ctrl-=", mac: "ctrl-="},
                 exec: () => {
                     this.zoomIn();
                 },
                 readOnly: true
            }, {
                 name: "zoomOut",
                 bindKey: {win: "ctrl--", mac: "ctrl--"},
                 exec: () => {
                     this.zoomOut();
                 },
                 readOnly: true
            }, {
                 name: "cutToBuffer",
                 bindKey: {win: "ctrl-k", mac: "ctrl-k"},
                 exec: () => {
                     this.cutToBuffer();
                 },
                 readOnly: false
            }, {
                 name: "pasteCutBuffer",
                 bindKey: {win: "ctrl-u", mac: "ctrl-u"},
                 exec: () => {
                     this.pasteCutBuffer();
                 },
                 readOnly: false
            }, {
                 name: "destroySession",
                 bindKey: {win: "ctrl-w", mac: "ctrl-w"},
                 exec: () => {
                     this.editor.session.destroy();
                 },
                 readOnly: false
            }, {
                 name: "openFiles",
                 bindKey: {win: "ctrl-o", mac: "ctrl-o"},
                 exec: () => {
                     this.openFiles();
                 },
                 readOnly: false
            }, {
                 name: "saveFile",
                 bindKey: {win: "ctrl-s", mac: "ctrl-s"},
                 exec: () => {
                     this.saveFile();
                 },
                 readOnly: false
            }, {
                 name: "saveFileAs",
                 bindKey: {win: "ctrl-shift-s", mac: "ctrl-shift-s"},
                 exec: () => {
                     this.saveFileAs();
                 },
                 readOnly: false
            }
        ]);


        // Note:  https://ajaxorg.github.io/ace-api-docs/interfaces/ace.Ace.EditorEvents.html
        this.editor.on("click", () => {
            this.updateInfoBar();
        });

        this.editor.on("input", () => {
            this.updateInfoBar();
        });

        this.editor.on("keyboardActivity", (e) => {
            switch(e.command.name) {
                case "golineup":
                case "golinedown":
                case "gotoleft":
                case "gotoright":
                    this.infoBarService.setInfoBarCursorPos(
                        this.editor.getCursorPosition()
                    );
                    break;
                default:
                    break;
            }
        });

        this.editor.on("focus", () => {
            this.editorsService.setActiveEditor(this.uuid);
        });

        this.editor.on("changeSession", (session) => {
            this.lspService.registerEditor(this.editor);
            this.updateInfoBar();
        });
    }

    public updateInfoBar() {
        this.infoBarService.setInfoBarFPath(this.activeFile?.path)
        this.infoBarService.setInfoBarCursorPos(
            this.editor.getCursorPosition()
        );
        this.infoBarService.setInfoBarFType(
            this.editor.session.getMode()["$id"]
        );
    }

    public newBuffer() {
        let buffer = ace.createEditSession([""]);
        this.editor.setSession(buffer);
        this.activeFile = null;
        this.updateInfoBar();
    }

}