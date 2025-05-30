import { Component, ElementRef, ViewChild, Input } from '@angular/core';

// Import Ace and its modes/themes so that `ace` global is defined
import * as ace from 'ace-builds/src-noconflict/ace';
import 'ace-builds/src-noconflict/theme-one_dark';
import "ace-builds/src-noconflict/ext-language_tools";

import { EditorsService } from '../../common/services/editor/editors.service';
import { LSPService } from '../../common/services/lsp.service';

import { EditorSettings } from "../../common/configs/editor.config";



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
export class AceEditorComponent {

    @Input() editorSettings!: typeof EditorSettings;
    @ViewChild('editor') editorElm!: ElementRef;
    editor!: any;
    uuid!: string;


    constructor(
        private editorsService: EditorsService,
        private lspService: LSPService
    ) {}


    public ngAfterViewInit(): void {
        this.loadAce();
    }

    public loadAce(): void {
        ace.config.set('basePath', this.editorSettings.BASE_PATH);

        this.editor = ace.edit( this.editorElm.nativeElement );
        this.editor.setOptions( this.editorSettings.CONFIG );
//        this.editor.commands.addCommands( this.editorSettings.KEYBINDINGS );

        // Note: https://github.com/mkslanc/ace-linters/blob/c286d85c558530aa1b0597d02108bc782abd4736/packages/ace-linters/src/language-provider.ts#L277
        //       found on focus ^ might have other signals we can watch like session being set, etc.
        this.editor.on("focus", () => {
            this.editorsService.setActiveEditor(this.uuid);
        });

//        this.editor.on("changeSession", (session) => {
//            console.log(session);
//            console.log(session.session["$modeId"]);
//        });
    }

    public registerEditorToLSPMode() {
        this.lspService.registerEditor(this.editor);
    }

}