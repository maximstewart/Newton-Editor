import { Component } from '@angular/core';
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
        'class': 'row tabs scroller'
    }
})
export class TabsComponent {
    private unsubscribe = new Subject<void>();

    activeTab!: string;
    tabs: any[] = [];
    newIndex: number = -1;


    constructor(
        private editorsService: EditorsService,
        private tabsService: TabsService
    ) {
    }

    public ngAfterViewInit(): void {
        this.tabsService.getData$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((data: ServiceMessage) => {
            if (data.action === "create-tab")
                this.createTab(data.message, data.uuid, data.data);
        });
    }

    ngOnDestroy(): void {
        this.unsubscribe.next();
        this.unsubscribe.complete();
    }

    private createTab(title: string, uuid: string, path: string): void {
        this.tabs.push({title: title, path: path, uuid: uuid})
    }

    handleAction(event: any): void {
        let target = event.target;

        if ( target.classList.contains("tab") ) {
            this.editorsService.setTabToEditor(
                event.srcElement.getAttribute("title")
            );
        } else if ( target.classList.contains("title") ) {
            this.editorsService.setTabToEditor(
                event.srcElement.parentElement.getAttribute("title")
            );
        } else if ( target.classList.contains("close-button") ) {
            this.closeTab(
                event.srcElement.parentElement.getAttribute("title")
            );
        }

    }

    closeTab(fpath: string): void {
        this.editorsService.closeTab(fpath);

        for (let i = 0; i < this.tabs.length; i++) {
            if (this.tabs[i].path == fpath) {
                this.tabs.splice(i, 1);
            }
        }

    }


    moved(event: any): void {
        let target = event.event.target;
        let fpath  = "";

        if ( target.classList.contains("title") ) {
            fpath = target.parentElement.getAttribute("title")
        } else if ( target.classList.contains("close-button") ) {
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

    dropped(event: CdkDragDrop<any>): void {
        if (this.newIndex == -1) return;

        moveItemInArray(this.tabs, event.previousIndex, this.newIndex);
        this.newIndex = -1;

        // event.currentIndex not updating for some reason...
        // moveItemInArray(this.tabs, event.previousIndex, event.currentIndex);
    }

}