import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { TabsComponent } from './editor/tabs/tabs.component';
import { EditorsComponent } from './editor/editors.component';



declare global {
    interface Window {
        electron: {
            node: () => Promise<string>,
            chrome: () => Promise<string>,
            electron: () => Promise<string>,
        },
        main: {
            onMenuActions: (arg0: any) => Promise<string>,
        },
        fs: {
            getLspConfigData: () => Promise<string>,
            getFileContents: (arg0: any) => Promise<string>,
            openFiles: (arg0) => Promise<string>,
            saveFile: (arg0: any, arg1: any) => Promise<string>,
            saveFileAs: (arg0: any) => Promise<string>,
            getPathForFile: any,
            onLoadFiles: (arg0: any) => Promise<string>,
        }
    }
}



@Component({
    selector: 'app-root',
    imports: [
        TabsComponent,
        EditorsComponent
    ],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css',
    host: {
        'class': 'row'
    }
})
export class AppComponent {
    title = 'Newton';

    constructor() {}

}