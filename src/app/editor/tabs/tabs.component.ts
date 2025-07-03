import { Component, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CdkDrag, CdkDragDrop, CdkDropList } from '@angular/cdk/drag-drop';
import { Subject, takeUntil } from 'rxjs';

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

    private tabsService: TabsService             = inject(TabsService);
    private changeDetectorRef: ChangeDetectorRef = inject(ChangeDetectorRef);

    tabs: any[] = this.tabsService.tabs;


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
            this.tabsService.sendEditorsServiceAMessage(
                "set-tab-to-editor",
                event.srcElement.getAttribute("title")
            );

        } else if ( target.classList.contains("title") ) {
            this.tabsService.sendEditorsServiceAMessage(
                "set-tab-to-editor",
                event.srcElement.parentElement.getAttribute("title")
            );
        } else if ( target.classList.contains("close-button") ) {
            this.tabsService.closeTab(
                event.srcElement.parentElement.getAttribute("title")
            );
        }

    }

    public createTab(title: string, uuid: string, path: string): void {
        this.tabsService.push({title: title, uuid: uuid, path: path});
        this.changeDetectorRef.detectChanges();
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

        this.tabsService.setNewTargetIndex(fpath);
    }

    protected dropped(event: CdkDragDrop<any>): void {
        this.tabsService.move(event.previousIndex);
    }

}