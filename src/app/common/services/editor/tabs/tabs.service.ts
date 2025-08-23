import { Injectable, inject } from '@angular/core';
import { moveItemInArray } from '@angular/cdk/drag-drop';
import { BehaviorSubject, ReplaySubject, Observable } from 'rxjs';

import { EditorsService } from '../editors.service';

import { ServiceMessage } from '../../../types/service-message.type';


@Injectable({
    providedIn: 'root'
})
export class TabsService {
    private messageSubject: ReplaySubject<ServiceMessage> = new ReplaySubject(1);

    private editorsService: EditorsService = inject(EditorsService);

    tabs: any[]      = [];
    newIndex: number = -1;


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
        if (this.tabs.length === 0 ) return;

        let i = this.tabs.indexOf(fpath);

        (i === 0) ? i = this.tabs.length - 1 : i -= 1;
        return this.tabs[i].path;
    }

    public getRightSiblingTab(fpath: string): string {
        if (this.tabs.length === 0 ) return;

        let i = this.tabs.indexOf(fpath);

        (i === (this.tabs.length - 1)) ? i = 0 : i += 1;
        return this.tabs[i].path;
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