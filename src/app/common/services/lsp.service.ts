import { Injectable } from '@angular/core';
import { BehaviorSubject, ReplaySubject, Observable } from 'rxjs';

import { AceLanguageClient, LanguageClientConfig } from 'ace-linters/build/ace-language-client';
import { LanguageProvider } from "ace-linters";



@Injectable({
    providedIn: 'root'
})
export class LSPService {
    lspConfigData!: {};
    languageProvider!: any;

    constructor() {
        this.loadLSPService();
    }

    private loadLSPService() {
        this.getLspConfigData().then((lspConfigData: string) => {
            this.lspConfigData = JSON.parse(lspConfigData);

            if (this.lspConfigData["message"]) {
                console.log(
                    "Warning: LSP this.lspConfigData is a 'message'",
                    this.lspConfigData
                );

                this.lspConfigData = {};
            }
        }).then(() => {
            this.loadLanguageProviders();
        });
    }

    public registerEditor(editor: any): void {
        this.languageProvider.registerEditor(editor);
    }

    private getLspConfigData(): Promise<string> {
        return window.fs.getLspConfigData();
    }

    private loadLanguageProviders(): void {
        this.languageProvider = this.getLanguageProviderWithClientServers();
//        this.languageProvider = this.getLanguageProviderWithWebWorker();
    }

    private getLanguageProviderWithClientServers() {
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
 
 
    private getLanguageProviderWithWebWorker() {
        let worker = new Worker(new URL('./webworker.js', import.meta.url));
        return LanguageProvider.create(worker);
    }
}