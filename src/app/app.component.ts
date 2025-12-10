import { Component, inject } from '@angular/core';

import { WebsocketService } from './common/services/websocket.service';

import { InfoBarComponent } from './editor/info-bar/info-bar.component';
import { TabsComponent } from './editor/tabs/tabs.component';
import { EditorsComponent } from './editor/editors.component';
import { SearchReplaceComponent } from "./editor/search-replace/search-replace.component";
import { MarkdownPreviewComponent } from "./editor/markdown-preview/markdown-preview.component";
import { LspManagerComponent } from "./editor/lsp-manager/lsp-manager.component";



@Component({
    selector: 'app-root',
    imports: [
        InfoBarComponent,
        TabsComponent,
        EditorsComponent,
        SearchReplaceComponent,
        MarkdownPreviewComponent,
        LspManagerComponent,
    ],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css',
    host: {
        'class': 'row'
    }
})
export class AppComponent {
    title = 'Newton';

    protected ws: WebsocketService = inject(WebsocketService);


    constructor() {
        this.checkIfNotElectronMode();
    }


    ngOnInit() {}

    checkIfNotElectronMode() {
        if (
            window.electron ||
            window.main     ||
            window.fs
        ) { return; }

        this.setupWebsocket();
        this.setupWindowBindings();
    }

    setupWindowBindings() {
        window.electron ??= {
            node: () => { return "" },
            chrome: () => { return "" },
            electron: () => { return "" },
        };

        window.main ??= {
            onMenuActions: () => {},
            onTerminalActions: () => {},
            quit: () => {},
            toggleFullScreen: () => {},
        };

        window.fs ??= {
            getLspConfigData: () => {
                return new Promise((resolve, reject) => {
                    resolve("{}");
                });
            },
            getFileContents: () => {},
            openFiles: () => {},
            saveFile: () => {},
            saveFileAs: () => {},
            chooseFolder: () => {},
            closeFile: () => {},
            getPathForFile: () => {},
            onLoadFiles: () => {},
            onUpdateFilePath: () => {},
            onSavedFile: () => {},
            onChangedFile: () => {},
            onDeletedFile: () => {},
        };
    }

    setupWebsocket() {
        // TODO: Set with dynamic address and port
        this.ws.connect('ws://localhost:7272').subscribe(msg => {
            console.log(msg);
            console.log(window.fs);
            // this.ws.send("{ 'text': 'Hello server!' }");
        });
    }

}