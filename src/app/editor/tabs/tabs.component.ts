import { Component, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CdkDrag, CdkDragDrop, CdkDropList, moveItemInArray } from '@angular/cdk/drag-drop';
import { Subject, takeUntil } from 'rxjs';

import { EditorsService } from '../../common/services/editor/editors.service';
import { TabsService } from '../../common/services/editor/tabs/tabs.service';

import { ServiceMessage } from '../../common/types/service-message.type';



@Component({
    selector: 'tabs',
    standalone: true,
    imports: [
        CommonModule,
        CdkDropList,
        CdkDrag,
    ],
    templateUrl: './tabs.component.html',
    styleUrl: './tabs.component.css',
    host: {
        'class': 'tabs scroller'
    }
})
export class TabsComponent {
    private unsubscribe: Subject<void>           = new Subject();

    private editorsService: EditorsService       = inject(EditorsService);
    private tabsService: TabsService             = inject(TabsService);
    private changeDetectorRef: ChangeDetectorRef = inject(ChangeDetectorRef);

    activeTab!: string;
    tabs: any[]      = [];
    newIndex: number = -1;


    constructor() {
    }

    private ngAfterViewInit(): void {
        this.loadSubscribers();
    }

    private ngOnDestroy(): void {
        this.unsubscribe.next();
        this.unsubscribe.complete();
    }

    private loadSubscribers() {
        this.tabsService.getMessage$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((message: ServiceMessage) => {
            if (message.action === "create-tab") {
                this.createTab(message.fileName, message.fileUUID, message.filePath);
            } else if (message.action === "file-changed") {
                let elm = document.querySelectorAll(`[title="${message.filePath}"]`)[1];
                elm.classList.add("file-changed");
                elm.classList.remove("file-deleted");
            } else if (message.action === "file-deleted") {
                let elm = document.querySelectorAll(`[title="${message.filePath}"]`)[1];
                elm.classList.add("file-deleted");
                elm.classList.remove("file-changed");
            } else if (message.action === "file-saved") {
                let elm = document.querySelectorAll(`[title="${message.filePath}"]`)[1];
                elm.classList.remove("file-deleted");
                elm.classList.remove("file-changed");
            }
        });
    }

    protected handleAction(event: any): void {
        let target = event.target;

        if ( target.classList.contains("tab") ) {
            this.sendEditorsServiceAMessage(
                "set-tab-to-editor",
                event.srcElement.getAttribute("title")
            );

        } else if ( target.classList.contains("title") ) {
            this.sendEditorsServiceAMessage(
                "set-tab-to-editor",
                event.srcElement.parentElement.getAttribute("title")
            );
        } else if ( target.classList.contains("close-button") ) {
            this.closeTab(
                event.srcElement.parentElement.getAttribute("title")
            );
        }

    }

    public createTab(title: string, uuid: string, path: string): void {
        this.tabs.push({title: title, uuid: uuid, path: path});
        this.changeDetectorRef.detectChanges();
    }

    public closeTab(fpath: string): void {
        this.sendEditorsServiceAMessage("close-tab", fpath);

        for (let i = 0; i < this.tabs.length; i++) {
            if (this.tabs[i].path == fpath) {
                this.tabs.splice(i, 1);
            }
        }

    }

    private moved(event: any): void {
        let target = event.event.target;
        let fpath  = "";

        if ( target.classList.contains("title") ||
            target.classList.contains("close-button")
        ) {
            fpath = target.parentElement.getAttribute("title")
        } else (
            fpath = target.getAttribute("title")
        )

        for (let i = 0; i < this.tabs.length; i++) {
            if (this.tabs[i].path == fpath) {
                this.newIndex = i;
            }
        }

    }

    protected dropped(event: CdkDragDrop<any>): void {
        if (this.newIndex == -1) return;

        moveItemInArray(this.tabs, event.previousIndex, this.newIndex);
        this.newIndex = -1;

        // event.currentIndex not updating for some reason...
        // moveItemInArray(this.tabs, event.previousIndex, event.currentIndex);
    }


    private sendEditorsServiceAMessage(action: string, fpath: string) {
        let message      = new ServiceMessage();
        message.action   = action;
        message.filePath = fpath;

        this.editorsService.sendMessage(message);
    }

}