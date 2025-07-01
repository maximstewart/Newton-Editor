import { Component } from "@angular/core";

// Import Ace and its modes/themes so that `ace` global is defined
import * as ace from "ace-builds/src-noconflict/ace";
import "ace-builds/src-noconflict/ext-settings_menu";
import "ace-builds/src-noconflict/ext-keybinding_menu";
import "ace-builds/src-noconflict/ext-command_bar";
import "ace-builds/src-noconflict/ext-prompt";
import "ace-builds/src-noconflict/ext-code_lens";
import "ace-builds/src-noconflict/ext-searchbox";
import "ace-builds/src-noconflict/ext-language_tools";
//import "ace-builds/src-noconflict/theme-one_dark";
//import "ace-builds/src-noconflict/theme-penguins_in_space";
import "ace-builds/src-noconflict/theme-gruvbox";

import { CodeViewBase } from './view.base';

import { NewtonFile } from '../../common/types/file.type';
import { ServiceMessage } from '../../common/types/service-message.type';



@Component({
    selector: 'code-view',
    standalone: true,
    imports: [
    ],
    templateUrl: './view.component.html',
    styleUrl: './view.component.css',
    host: {
        'class': 'col zero-margin-padding scroller'
    }
})
export class CodeViewComponent extends CodeViewBase {


    constructor() {
        super();
    }


    private ngAfterViewInit(): void {
        this.loadAce();
    }

    private loadAce(): void {
        this.configAceAndBindToElement()

        if (this.isDefault) {
            this.editorsService.setActiveEditor(this.uuid);
            this.addActiveStyling();
        }

        if (this.isMiniMap) {
            this.setAsMiniMapView();
            return;
        }

        this.loadAceKeyBindings();
        this.loadAceEventBindings();
    }

    private configAceAndBindToElement(): void {
        this.editorSettings = this.editorsService.editorSettings;

        ace.config.set('basePath', this.editorSettings.BASE_PATH);

        this.editor = ace.edit( this.editorElm.nativeElement );
        this.editor.setOptions( this.editorSettings.CONFIG );
        this.editorsService.set(this.uuid, this);
    }

    private loadAceKeyBindings(): void {
        let keyBindings = [];
        for (let i = 0; i < this.editorSettings.KEYBINDINGS.length; i++) {
            let keyBinding = this.editorSettings.KEYBINDINGS[i];
            keyBindings.push(
                {
                     name: keyBinding.name,
                     bindKey: keyBinding.bindKey,
                     exec: (keyBinding.name && keyBinding?.service) ?
                         () => (
                             this[keyBinding?.service][keyBinding.name]()
                         )
                     :
                         (this[keyBinding.name]) ?
                             () => (
                                 this[keyBinding.name]()
                             )
                         :
                             () => (
                                 console.log(
                                    `Name: ${keyBinding.name}, is not mapping to a method OR mapping to a Service: ${keyBinding?.service} and Name: ${keyBinding.name}.`
                                )
                             )
                     ,
                     readOnly: keyBinding.readOnly
                }
            );
        }

        this.editor.commands.addCommands( keyBindings );
    }

    private loadAceEventBindings(): void {

        // Note:  https://ajaxorg.github.io/ace-api-docs/interfaces/ace.Ace.EditorEvents.html
        this.editor.on("focus", (e) => {
            let message        = new ServiceMessage();
            message.action     = "set-active-editor";
            message.editorUUID = this.uuid;

            this.editorsService.sendMessage(message);

            this.updateInfoBar();
        });

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

        this.editor.on("change", () => {
            if (!this.activeFile) return;

            let message      = new ServiceMessage();
            message.action   = "file-changed";
            message.filePath = this.activeFile.path;
            this.tabsService.sendMessage(message);
        });

        this.editor.on("changeSession", (session) => {
            this.updateInfoBar();
        });
    }


    public newSession() {
        this.activeFile = null;
        let session     = ace.createEditSession([""]);
        this.editor.setSession(session);
    }

    public assignSession(file: NewtonFile) {
        if (!file) return;

        this.activeFile = file;
        this.editor.setSession(file.session);
    }

    public cloneSession(file: NewtonFile) {
        if (!file) return;

        this.activeFile = file;
        let session     = ace.createEditSession(file.session.getValue());

        session.setMode( file.session.getMode()["$id"] );
        this.editor.setSession(session);
    }

    protected openFiles() {
        let startDir = "";
        if (this.activeFile) {
            let pathParts = this.activeFile.path.split("/");
            pathParts.pop();
            startDir = pathParts.join( '/' );
        }

        window.fs.openFiles(startDir);
    }

    protected saveFile() {
        if (!this.activeFile) {
            this.saveFileAs();
            return;
        }

        const text = this.activeFile.session.getValue();
        window.fs.saveFile(this.activeFile.path, text);
    }

    protected saveFileAs() {
        window.fs.saveFileAs().then((path: string) => {
            if (!path) return;

            let file: NewtonFile = new File([""], path, {});
            const text           = this.editor.session.getValue();

            window.fs.saveFile(path, text);
            this.filesService.addFile(
                path,
                file,
                false,
                text
            ).then(() => {
                this.activeFile = this.filesService.get(path);
                this.editor.setSession(this.activeFile.session);
                this.filesService.addTab(this.activeFile);
            });

        });
    }

    protected cutToBuffer() {
        if (this.timerId) { clearTimeout(this.timerId); }

        const cursorPosition = this.editor.getCursorPosition();
        let lineText         = this.editor.session.getLine(cursorPosition.row);
        this.cutBuffer       += `${lineText}\n`;

        this.editor.session.removeFullLines(cursorPosition.row, cursorPosition.row)
        this.setBufferClearTimeout();
    }

    protected pasteCutBuffer() {
        if (this.timerId) { clearTimeout(this.timerId); }

        this.editor.insert(this.cutBuffer, true);
        this.setBufferClearTimeout();
    }

    private setBufferClearTimeout(timeout: number = 5000) {
        this.timerId = setTimeout(() => {
            this.cutBuffer = "";
            this.timerId   = -1;
        }, timeout);
    }

}