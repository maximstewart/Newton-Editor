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

    workspaceFolder: string  = "";
    lspConfigDataStr: string = "";
    languageProviders: {}    = {};


    constructor() {
    }


    public loadLspConfigData(): Promise<string | void> {
        return this.getLspConfigData().then((lspConfigData: string) => {
            this.lspConfigDataStr = lspConfigData;
            return lspConfigData;
        });
    }

    public registerEditorToLSPClient(editor: any) {
        let mode = this.getMode(editor.session);

        if ( this.languageProviders[mode] ) {
            this.languageProviders[mode].registerEditor(editor);
            return;
        }

        this.languageProviders[mode]?.registerEditor(editor);
    }

    private getLspConfigData(): Promise<string> {
        return window.fs.getLspConfigData();
    }

    private parseAndReturnLSPConfigData(): {} {
        let configData = JSON.parse(
            this.lspConfigDataStr.replaceAll("{workspace.folder}", this.workspaceFolder)
        );

        if (configData["message"]) {
            console.warn(
                "Warning: LSP this.lspConfigDataStr is a 'message'",
                this.lspConfigDataStr
            );

            configData = {};
        }

        return configData;
    }

    private getInitializationOptions(mode: string, configData: {}): {} {
        let _initializationOptions = {};

        if ( Object.keys(configData).length !== 0 && configData[mode] ) {
            _initializationOptions = configData[mode]["initialization-options"];
        }

        return _initializationOptions;
    }

    public createLanguageProviderWithClientServer(mode: string): LanguageProvider {
        if ( this.languageProviders[mode] ) return;
        let servers: LanguageClientConfig[] = [];

        try {
            let configData             = this.parseAndReturnLSPConfigData();
            let _initializationOptions = this.getInitializationOptions(mode, configData);
            servers = [
                {
                    module: () => import("ace-linters/build/language-client"),
                    modes: mode,
                    type: "socket",
                    socket: new WebSocket( configData[mode]["socket"] ),
                    initializationOptions: _initializationOptions
                }
            ];
        } catch(error) {
            console.error(
                "Error: Language Server could not be loaded OR doesn't exist in Newton-LSP config setup...",
            );

            return;
        }

        this.languageProviders[mode] = AceLanguageClient.for(servers);
        // this.languageProviders[mode].requireFilePath = true;
        this.languageProviders[mode].changeWorkspaceFolder(this.workspaceFolder);
        return this.languageProviders[mode];
    }

    private getLanguageProviderWithWebWorker(): LanguageProvider {
        let worker = new Worker(new URL('./webworker.js', import.meta.url));
        return LanguageProvider.create(worker);
    }

    public setSessionFilePath(session: any, filePath: string = "") {
        if ( !session || !filePath ) return;
        let mode = this.getMode(session);
        if ( !this.languageProviders[mode] ) return;
        this.languageProviders[mode].setSessionFilePath(session, filePath);
    }

    public getMode(session: any): string {
        return session.getMode()["$id"].replace("ace/mode/", "");
    }

    public closeDocument(session: any) {
        if ( !session ) return;
        let mode = this.getMode(session);
        if ( !this.languageProviders[mode] ) return;
        this.languageProviders[mode].closeDocument(session);
    }

    public sendMessage(data: ServiceMessage): void {
        this.messageSubject.next(data);
    }

    public getMessage$(): Observable<ServiceMessage> {
        return this.messageSubject.asObservable();
    }

}