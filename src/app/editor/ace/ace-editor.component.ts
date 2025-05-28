import { Component, ElementRef, ViewChild, Input } from '@angular/core';

import { AceLanguageClient, LanguageClientConfig } from 'ace-linters/build/ace-language-client';

// Import Ace and its modes/themes so that `ace` global is defined
import * as ace from 'ace-builds/src-noconflict/ace';
import 'ace-builds/src-noconflict/theme-one_dark';
import "ace-builds/src-noconflict/ext-language_tools";

import { LanguageProvider } from "ace-linters";

import { EditorSettings } from "../../common/configs/editor.config";

import { EditorsService } from '../../common/services/editor/editors.service';
import { ServiceMessage } from '../../common/types/service-message.type';



@Component({
    selector: 'ace-editor',
    standalone: true,
    imports: [
    ],
    templateUrl: './ace-editor.component.html',
    styleUrl: './ace-editor.component.css',
    host: {
        'class': 'col',
        '(click)': 'onClick($event)'
    }
})
export class AceEditorComponent {

    @Input() editorSettings!: typeof EditorSettings;
    @ViewChild('editor') editorElm!: ElementRef;
    editor!: any;
    uuid!: string;
    lspConfigData!: {};


    constructor(private editorsService: EditorsService) {
    }


    public ngAfterViewInit(): void {
        this.loadAce();
        this.loadLanguageProviders();
    }

    public loadAce(): void {
        ace.config.set('basePath', this.editorSettings.BASE_PATH);

        this.editor = ace.edit( this.editorElm.nativeElement );
        this.editor.setOptions( this.editorSettings.CONFIG );
//        this.editor.commands.addCommands( this.editorSettings.KEYBINDINGS );
    }

    protected onClick(event: any) {
        let message        = new ServiceMessage();
        message.action     = "set-editor";
        message.message    = this.uuid;
        message.uuid       = this.uuid;

        this.editorsService.setData(message);
    }

    public loadLanguageProviders(): void {
        let languageProvider = this.getLanguageProviderWithClientServers();
//        let languageProvider = this.getLanguageProviderWithWebWorker();
        languageProvider.registerEditor(this.editor);

    }



    public getLanguageProviderWithClientServers() {
        let _initializationOptions = {};

        if (Object.keys(this.lspConfigData).length !== 0) {
//            _initializationOptions = this.lspConfigData[ this.editor.session.getMode() ]["initialization-options"];
            _initializationOptions = this.lspConfigData[ "python" ]["initialization-options"];
        }

        let servers: LanguageClientConfig[] = [
            {
                module: () => import("ace-linters/build/language-client"),
                modes: "python",
                type: "socket",
                socket: new WebSocket("ws://127.0.0.1:9999/python"),
//                socket: new WebSocket("ws://127.0.0.1:9999/?name=pylsp"),
                initializationOptions: _initializationOptions
            }
        ];

        return AceLanguageClient.for(servers);
    }
 
 
    public getLanguageProviderWithWebWorker() {
        let worker = new Worker(new URL('./webworker.js', import.meta.url));
        return LanguageProvider.create(worker);
    }

}