import { Injectable } from '@angular/core';
import { ReplaySubject, Observable } from 'rxjs';

import { AceLanguageClient, LanguageClientConfig } from 'ace-linters/build/ace-language-client';
import { LanguageProvider } from "ace-linters";

import { ServiceMessage } from '../../../types/service-message.type';



@Injectable({
    providedIn: 'root'
})
export class LspManagerService {
    private messageSubject: ReplaySubject<ServiceMessage> = new ReplaySubject<ServiceMessage>(1);

    lspConfigData!: {};
    languageProviders: {} = {};


    constructor() {
    }


    public loadLspConfigData(): Promise<string | void> {
        return this.getLspConfigData().then((lspConfigData: string) => {
            this.lspConfigData = JSON.parse(lspConfigData);

            if (this.lspConfigData["message"]) {
                console.log(
                    "Warning: LSP this.lspConfigData is a 'message'",
                    this.lspConfigData
                );

                this.lspConfigData = {};
            }

            return lspConfigData;
        });
    }

    public registerEditor(editor: any): void {
        let modeParts = editor.getSession()["$modeId"].split("/");
        let mode      = modeParts[ modeParts.length - 1 ];

        if ( !this.languageProviders[mode] ) {
            this.languageProviders[mode] = this.getLanguageProviderWithClientServer(mode);
        }

        this.languageProviders[mode].registerEditor(editor);
    }

    private getLspConfigData(): Promise<string> {
        return window.fs.getLspConfigData();
    }

    private getLanguageProviderWithClientServer(mode: string) {
        let _initializationOptions = {};

        if ( Object.keys(this.lspConfigData).length !== 0 && this.lspConfigData[mode] ) {
            _initializationOptions = this.lspConfigData[mode]["initialization-options"];
        }

        let servers: LanguageClientConfig[] = [
            {
                module: () => import("ace-linters/build/language-client"),
                modes: mode,
                type: "socket",
                socket: new WebSocket(`ws://127.0.0.1:9999/${mode}`),
                // socket: new WebSocket("ws://127.0.0.1:9999/?name=pylsp"),
                initializationOptions: _initializationOptions
            }
        ];

        return AceLanguageClient.for(servers);
    }

    private getLanguageProviderWithWebWorker() {
        let worker = new Worker(new URL('./webworker.js', import.meta.url));
        return LanguageProvider.create(worker);
    }

    protected setSessionFilePath(session: any, mode: string = "", filePath: string = "") {
        if ( !session || !mode || !filePath || !this.languageProviders[mode] ) return;
        this.languageProviders[mode].setSessionFilePath(session, filePath);
    }

    protected closeDocument(session: any, mode: string) {
        if ( !session || !mode || !this.languageProviders[mode] ) return;
        this.languageProviders[mode].closeDocument(session);
    }

    public sendMessage(data: ServiceMessage): void {
        this.messageSubject.next(data);
    }

    public getMessage$(): Observable<ServiceMessage> {
        return this.messageSubject.asObservable();
    }

}