import { Component } from '@angular/core';

import { InfoBarComponent } from './editor/info-bar/info-bar.component';
import { TabsComponent } from './editor/tabs/tabs.component';
import { EditorsComponent } from './editor/editors.component';
import { FilesModalComponent } from "./common/components/modals/files/files-modal.component";



@Component({
    selector: 'app-root',
    imports: [
        InfoBarComponent,
        TabsComponent,
        EditorsComponent,
        FilesModalComponent
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