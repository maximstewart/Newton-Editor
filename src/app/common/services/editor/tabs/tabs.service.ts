import { Injectable, inject } from '@angular/core';
import { moveItemInArray } from '@angular/cdk/drag-drop';
import { BehaviorSubject, ReplaySubject, Observable } from 'rxjs';

import { EditorsService } from '../editors.service';

import { ServiceMessage } from '../../../types/service-message.type';


@Injectable({
    providedIn: 'root'
})
export class TabsService {
    private messageSubject: ReplaySubject<ServiceMessage> = new ReplaySubject<ServiceMessage>(1);

    private editorsService: EditorsService = inject(EditorsService);

    tabs: any[]      = [];
    newIndex: number = -1;

    constructor() {}


    public push(tabData: {}): void {
        this.tabs.push(tabData);
    }

    public closeTab(fpath: string): void {
        this.sendEditorsServiceAMessage("close-tab", fpath);

        for (let i = 0; i < this.tabs.length; i++) {
            if (this.tabs[i].path == fpath) {
                this.splice(i);
                break;
            }
        }
    }

    public sendEditorsServiceAMessage(action: string, fpath: string) {
        let message      = new ServiceMessage();
        message.action   = action;
        message.filePath = fpath;

        this.editorsService.sendMessage(message);
    }

    public getLeftSiblingTab(fpath: string): string {
        let size = this.tabs.length;
        let i    = 0;

        for (; i < size; i++) {
            if (this.tabs[i].path == fpath) {
                break;
            }
        }

        if ( !(size > 1) ) {
            return "";
        }

        if ( i === 0 ) {
            return this.tabs[i + 1].path;
        }

        return this.tabs[i - 1].path;
    }

    public getRightSiblingTab(fpath: string): string {
        let size = this.tabs.length;
        let i    = 0;

        for (; i < size; i++) {
            if (this.tabs[i].path == fpath) {
                break;
            }
        }

        if ( !(size > 1) ) {
            return "";
        }

        if ( i === (size - 1) ) {
            return this.tabs[i - 1].path;
        }

        return this.tabs[i + 1].path;
    }

    public setNewTargetIndex(fpath: string): void {
        for (let i = 0; i < this.tabs.length; i++) {
            if (this.tabs[i].path == fpath) {
                this.newIndex = i;
                break;
            }
        }
    }

    public move(oldIndex: number): void {
        if (this.newIndex == -1) return;

        moveItemInArray(this.tabs, oldIndex, this.newIndex);
        this.newIndex = -1;

        // event.currentIndex not updating for some reason...
        // moveItemInArray(this.tabs, event.previousIndex, event.currentIndex);
    }

    public splice(index: number): void {
        this.tabs.splice(index, 1);
    }


    public sendMessage(data: ServiceMessage): void {
        this.messageSubject.next(data);
    }

    public getMessage$(): Observable<ServiceMessage> {
        return this.messageSubject.asObservable();
    }
}