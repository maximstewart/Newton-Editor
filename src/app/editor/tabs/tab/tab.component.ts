import { Component } from '@angular/core';



@Component({
    selector: 'tab',
    standalone: true,
    imports: [
    ],
    templateUrl: './tab.component.html',
    styleUrl: './tab.component.css',
    host: {
        'class': 'col'
//        'class': 'col tab'
    }
})
export class TabComponent {

    title: string;


    constructor() {
        this.title = "[NO TITLE]";
    }

    ngOnDestroy() {
    }


}