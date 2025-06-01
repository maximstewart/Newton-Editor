import { Component } from '@angular/core';

// Import Ace and its modes/themes so that `ace` global is defined
import * as ace from 'ace-builds/src-noconflict/ace';
import 'ace-builds/src-noconflict/theme-one_dark';
import "ace-builds/src-noconflict/ext-language_tools";

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
        private editorsService: EditorsService,
        private lspService: LSPService
    ) {
        super();
    }


    public ngAfterViewInit(): void {
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
                 readOnly: true
             }, {
                 name: "movelinesDown",
                 bindKey: {win: "ctrl-down", mac: "ctrl-down"},
                 exec: () => {
                     this.movelinesDown();
                 },
                 readOnly: true
             },
             {
                 name: "duplicateLines",
                 bindKey: {win: "ctrl-d", mac: "ctrl-d"},
                 exec: () => {
                     this.duplicateLines();
                 },
                 readOnly: true
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
                 readOnly: true
            }, {
                 name: "pasteCutBuffer",
                 bindKey: {win: "ctrl-u", mac: "ctrl-u"},
                 exec: () => {
                     this.pasteCutBuffer();
                 },
                 readOnly: true
            }, {
                 name: "destroySession",
                 bindKey: {win: "ctrl-w", mac: "ctrl-w"},
                 exec: () => {
                     this.editor.session.destroy();
                 },
                 readOnly: true
            }, {
                 name: "openFiles",
                 bindKey: {win: "ctrl-o", mac: "ctrl-o"},
                 exec: () => {
                     this.openFiles();
                 },
                 readOnly: true
            }, {
                 name: "saveFile",
                 bindKey: {win: "ctrl-s", mac: "ctrl-s"},
                 exec: () => {
                     this.saveFile();
                 },
                 readOnly: true
            }, {
                 name: "saveFileAs",
                 bindKey: {win: "ctrl-shift-s", mac: "ctrl-shift-s"},
                 exec: () => {
                     this.saveFileAs();
                 },
                 readOnly: true
            }
        ]);

        // Note: https://github.com/mkslanc/ace-linters/blob/c286d85c558530aa1b0597d02108bc782abd4736/packages/ace-linters/src/language-provider.ts#L277
        //       found on focus ^ might have other signals we can watch like session being set, etc.
        this.editor.on("focus", () => {
            this.editorsService.setActiveEditor(this.uuid);
        });

        this.editor.on("changeSession", (session) => {
            this.lspService.registerEditor(this.editor);
        });
    }

}