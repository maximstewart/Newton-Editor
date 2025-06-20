import { Component } from "@angular/core";

// Import Ace and its modes/themes so that `ace` global is defined
import * as ace from "ace-builds/src-noconflict/ace";
import "ace-builds/src-noconflict/ext-settings_menu";
import "ace-builds/src-noconflict/ext-keybinding_menu";
import "ace-builds/src-noconflict/ext-command_bar";
import "ace-builds/src-noconflict/ext-language_tools";
import "ace-builds/src-noconflict/theme-one_dark";
import "ace-builds/src-noconflict/theme-dracula";

import { InfoBarService } from '../../common/services/editor/info-bar/info-bar.service';
import { FilesModalService } from '../../common/services/editor/modals/files-modal.service';
import { LSPService } from '../../common/services/lsp.service';
import { TabsService } from '../../common/services/editor/tabs/tabs.service';
import { EditorsService } from '../../common/services/editor/editors.service';

import { NewtonEditorBase } from './newton-editor.base';

import { ServiceMessage } from '../../common/types/service-message.type';



@Component({
    selector: 'newton-editor',
    standalone: true,
    imports: [
    ],
    templateUrl: './newton-editor.component.html',
    styleUrl: './newton-editor.component.css',
    host: {
        'class': 'col col-6'
    }
})
export class NewtonEditorComponent extends NewtonEditorBase {


    constructor(
        private infoBarService: InfoBarService,
        private editorsService: EditorsService,
        private lspService: LSPService,
        private tabsService: TabsService,
        private filesModalService: FilesModalService
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

        // Note:  https://ajaxorg.github.io/ace-api-docs/interfaces/ace.Ace.EditorEvents.html
        this.editor.on("focus", (e) => {
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

        this.editor.on("focus", () => {
            let message        = new ServiceMessage();
            message.action     = "set-active-editor";
            message.editorUUID = this.uuid;

            this.editorsService.sendMessage(message);
        });

        this.editor.on("change", () => {
            let message      = new ServiceMessage();
            message.action   = "file-changed";
            message.filePath = this.activeFile.path;
            this.tabsService.sendMessage(message);
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

    public selectLeftEditor() {
        let message        = new ServiceMessage();
        message.action     = "select-left-editor";
        message.editorUUID = this.uuid;

        this.editorsService.sendMessage(message);
    }

    public selectRightEditor() {
        let message        = new ServiceMessage();
        message.action     = "select-right-editor";
        message.editorUUID = this.uuid;

        this.editorsService.sendMessage(message);
    }

    public moveSessionLeft() {
        let message        = new ServiceMessage();
        message.action     = "move-session-left";
        message.editorUUID = this.uuid;

        this.editorsService.sendMessage(message);
    }

    public moveSessionRight() {
        let message        = new ServiceMessage();
        message.action     = "move-session-right";
        message.editorUUID = this.uuid;

        this.editorsService.sendMessage(message);
    }

}