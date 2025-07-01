import { Component, inject } from "@angular/core";
import { CommonModule } from "@angular/common";

import { Subject, takeUntil } from 'rxjs';

import * as bootstrap from "bootstrap";

import AceDiff from 'ace-diff';

import 'ace-diff/dist/ace-diff.min.css';
import 'ace-diff/dist/ace-diff-dark.min.css';



@Component({
    selector: 'diff-modal',
    standalone: true,
    imports: [
        CommonModule
    ],
    templateUrl: './diff-modal.component.html',
    styleUrl: './diff-modal.component.css',
    host: {
        'class': ''
    }
})
export class DiffModalComponent {

    diffModal!: bootstrap.Modal;


    constructor() {
    }


    private ngAfterViewInit(): void {
        this.loadDiffView();
        this.loadSubscribers();
    }

    private loadDiffView() {
        // Notes:  https://github.com/ace-diff/ace-diff
        //  https://ajaxorg.github.io/ace-api-docs/classes/src_ext_diff_diff_view.DiffView.html#scrollB
        /*
        const differ = new AceDiff({
            ace: window.ace
                element: '.diff-view',
            left: {
                content: 'your first file content here',
            },
            right: {
                content: 'your second file content here',
            },
        });
        */
    }

    private loadSubscribers() {
    }

    private createModal() {
        this.diffModal = new bootstrap.Modal("#diffModal", {});
    }

    public showModal() {
        this.diffModal?.toggle();
    }

}