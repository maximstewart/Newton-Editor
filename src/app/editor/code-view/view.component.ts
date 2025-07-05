import { Component } from "@angular/core";

// Import Ace and its modes/themes so that `ace` global is defined
import * as ace from "ace-builds/src-min-noconflict/ace";
import "ace-builds/src-min-noconflict/ext-settings_menu";
import "ace-builds/src-min-noconflict/ext-keybinding_menu";
import "ace-builds/src-min-noconflict/ext-command_bar";
import "ace-builds/src-min-noconflict/ext-prompt";
import "ace-builds/src-min-noconflict/ext-code_lens";
// import "ace-builds/src-min-noconflict/ext-searchbox";
import "ace-builds/src-min-noconflict/ext-language_tools";
// import "ace-builds/src-min-noconflict/theme-one_dark";
// import "ace-builds/src-min-noconflict/theme-penguins_in_space";
import "ace-builds/src-min-noconflict/theme-gruvbox";

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

        this.aceApi = ace;
    }


    private ngAfterViewInit(): void {
        this.loadAce();
    }

    private loadAce(): void {
        this.configAceAndBindToElement()

        if (this.isDefault) {
            this.editorsService.setActiveEditor(this.uuid);
            this.addActiveStyling();
            this.editor.focus();
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
            message.rawData    = this.editor;

            this.editorsService.sendMessage(message);
            this.searchReplaceService.sendMessage(message);

            message            = new ServiceMessage();
            message.action     = "set-active-editor";
            message.rawData    = this;
            this.markdownPreviewService.sendMessage(message);

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
            if (this.debounceId) { clearTimeout(this.debounceId); }
            this.setDebounceTimeout();

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


    public assignSession(file: NewtonFile) {
        if (!file) return;

        this.activeFile = file;
        this.editor.setSession(file.session);
    }

    public cloneSession(file: NewtonFile) {
        if (!file) return;

        this.activeFile = file;
        let session     = this.aceApi.createEditSession(file.session.getValue());

        session.setMode( file.session.getMode()["$id"] );
        this.editor.setSession(session);
    }

    private setDebounceTimeout(timeout: number = null) {
        this.debounceId = setTimeout(() => {
            this.editorsService.miniMapView.editor.session.setValue(
                this.editor.session.getValue()
            );

            this.debounceId = -1;
        }, (timeout) ? timeout : this.debounceWait);
    }

}