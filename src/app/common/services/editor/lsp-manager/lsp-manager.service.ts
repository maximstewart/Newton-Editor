import { Injectable } from '@angular/core';
import { ReplaySubject, Observable } from 'rxjs';

import { CompletionProvider } from "ace-builds/src-min-noconflict/ace";
import { CommandBarTooltip } from "ace-builds/src-min-noconflict/ext-command_bar";
import { InlineAutocomplete } from "ace-builds/src-min-noconflict/ext-inline_autocomplete";

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


    public loadLspConfigData(): Promise<string | void> {
        return this.getLspConfigData().then((lspConfigData: string) => {
            this.lspConfigDataStr = lspConfigData;
            return lspConfigData;
        });
    }

    public registerEditorToLSPClient(editor: any) {
        let mode = this.getMode(editor.session);

        this.languageProviders[mode]?.registerEditor(
            editor,
            editor.session.lspConfig
        );
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
        let initializationOptions = {};

        if ( Object.keys(configData).length !== 0 && configData[mode] ) {
            initializationOptions = configData[mode]["initialization-options"];
        }

        return initializationOptions;
    }

    public createLanguageProviderWithClientServer(mode: string): LanguageProvider {
        if ( this.languageProviders[mode] ) return;
        let servers: LanguageClientConfig[] = [];

        try {
            let lspConfigData         = this.parseAndReturnLSPConfigData();
            let initializationOptions = this.getInitializationOptions(mode, lspConfigData);
            servers = [
                {
                    module: () => import("ace-linters/build/language-client"),
                    modes: mode,
                    type: "socket",
                    socket: new WebSocket( lspConfigData[mode]["socket"] ),
                    initializationOptions: initializationOptions
                }
            ];
        } catch(error) {
            console.error(
                "Error: Language Server could not be loaded OR doesn't exist in Newton-LSP config setup...",
            );

            return;
        }

        this.languageProviders[mode] = AceLanguageClient.for(
            servers,
            {
                workspacePath: this.workspaceFolder,
                functionality: {
                    hover: true,
                    completion: {
                        overwriteCompleters: true,
                        lspCompleterOptions: {
                            triggerCharacters: {
                                add: [
                                    " ",
                                    ".",
                                    "@"
                                ]
                            }
                        }
                    },
                    // inlineCompletion: {
                    //     overwriteCompleters: true
                    // },
                    completionResolve: true,
                    format: true,
                    documentHighlights: true,
                    signatureHelp: true,
                    semanticTokens: true,
                    codeActions: true
                },
                //  aceComponents: {
                //     InlineAutocomplete,
                //     CommandBarTooltip,
                //     CompletionProvider
                // },
                manualSessionControl: true
            }
        );

        return this.languageProviders[mode];
    }

    public closeLanguageProviderWithClientServer(mode: string): LanguageProvider {
        if ( !this.languageProviders[mode] ) return;

        let connection = this.languageProviders[mode];
        delete this.languageProviders[mode];
        connection.closeConnection();
    }

    private getLanguageProviderWithWebWorker(): LanguageProvider {
        let worker = new Worker(new URL('./webworker.js', import.meta.url));
        return LanguageProvider.create(worker);
    }

    public registerSession(editor: any) {
        let mode = this.getMode(editor.session);
        if ( !this.languageProviders[mode] ) return;

        this.languageProviders[mode].registerSession(
            editor.session,
            editor,
            editor.session.lspConfig
        );
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