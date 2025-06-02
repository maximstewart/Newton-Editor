import { Component } from '@angular/core';

import { EditorsService } from '../../../common/services/editor/editors.service';



@Component({
    selector: 'tab',
    standalone: true,
    imports: [
    ],
    templateUrl: './tab.component.html',
    styleUrl: './tab.component.css',
    host: {
        'class': ''
    }
})
export class TabComponent {

    title: string;
    path: string;
    ref: any;


    constructor(
        private editorsService: EditorsService,
    ) {
        this.title = "[NO TITLE]";
    }

    ngOnDestroy() {
    }

    setTabToEditor() {
        this.editorsService.setTabToEditor(this.path);
    }

    closeTab() {
        this.editorsService.closeTab(this.path);
        this.ref.destroy();
    }
}