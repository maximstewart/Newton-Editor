import { Component } from '@angular/core';

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

    constructor() {}

}