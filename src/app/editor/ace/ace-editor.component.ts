import { Component, ElementRef, ViewChild, Input } from '@angular/core';

// Import Ace and its modes/themes so that `ace` global is defined
import * as ace from 'ace-builds/src-noconflict/ace';
import 'ace-builds/src-noconflict/theme-one_dark';
import "ace-builds/src-noconflict/ext-language_tools";

import { EditorSettings } from "../../common/configs/editor.config";
import { ServiceMessage } from '../../common/types/service-message.type';

import { EditorsService } from '../../common/services/editor/editors.service';
import { LSPService } from '../../common/services/lsp.service';



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

        this.editor.on("focus", () => {
            this.editorsService.setActiveEditor(this.uuid);
        });

    }

    public registerEditorToLSP() {
        this.lspService.registerEditor(this.editor);
    }

}