import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { InfoBarComponent } from './editor/info-bar/info-bar.component';
import { TabsComponent } from './editor/tabs/tabs.component';
import { EditorsComponent } from './editor/editors.component';



@Component({
    selector: 'app-root',
    imports: [
        InfoBarComponent,
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