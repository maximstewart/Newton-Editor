import { Injectable } from '@angular/core';
import { BehaviorSubject, ReplaySubject, Observable } from 'rxjs';

import { ServiceMessage } from '../../types/service-message.type';



@Injectable({
    providedIn: 'root'
})
export class EditorsService {
    private messageSubject: ReplaySubject<ServiceMessage> = new ReplaySubject<ServiceMessage>(1);
    private activationSubject: ReplaySubject<string>      = new ReplaySubject<string>(1);
    private switchSessionSubject: ReplaySubject<string>   = new ReplaySubject<string>(1);
    private closeTabSubject: ReplaySubject<string>        = new ReplaySubject<string>(1);


    constructor() {}

    setData(data: ServiceMessage): void {
        this.messageSubject.next(data);
    }

    getData$(): Observable<ServiceMessage> {
        return this.messageSubject.asObservable();
    }

    setActiveEditor(data: string): void {
        this.activationSubject.next(data);
    }

    newActiveEditor$(): Observable<string> {
        return this.activationSubject.asObservable();
    }

    setTabToEditor(data: string): void {
        this.switchSessionSubject.next(data);
    }

    loadTabToEditor$(): Observable<string> {
        return this.switchSessionSubject.asObservable();
    }

    closeTab(data: string): void {
        this.closeTabSubject.next(data);
    }

    closeTabRequested$(): Observable<string> {
        return this.closeTabSubject.asObservable();
    }
}