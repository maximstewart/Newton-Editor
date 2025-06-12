import { Injectable } from '@angular/core';
import { BehaviorSubject, ReplaySubject, Observable } from 'rxjs';

import { ServiceMessage } from '../../../types/service-message.type';


@Injectable({
    providedIn: 'root'
})
export class InfoBarService {
    private dataSubject: ReplaySubject<ServiceMessage> = new ReplaySubject<ServiceMessage>(1);
    private fpathSubject: ReplaySubject<string> = new ReplaySubject<string>(1);
    private cursorPosSubject: ReplaySubject<any> = new ReplaySubject<any>(1);
    private encodeingSubject: ReplaySubject<string> = new ReplaySubject<string>(1);
    private ftypeSubject: ReplaySubject<string> = new ReplaySubject<string>(1);


    constructor() {}


    setData(data: ServiceMessage): void {
        this.dataSubject.next(data);
    }

    getData$(): Observable<ServiceMessage> {
        return this.dataSubject.asObservable();
    }

    setInfoBarFPath(data: string): void {
        this.fpathSubject.next(data);
    }

    updateInfoBarFPath$(): Observable<string> {
        return this.fpathSubject.asObservable();
    }

    setInfoBarCursorPos(data: any): void {
        this.cursorPosSubject.next(data);
    }

    updateInfoBarCursorPos$(): Observable<any> {
        return this.cursorPosSubject.asObservable();
    }

    setInfoBarEncodeing(data: string): void {
        this.encodeingSubject.next(data);
    }

    updateInfoBarEncodeing$(): Observable<string> {
        return this.encodeingSubject.asObservable();
    }

   setInfoBarFType(data: string): void {
        this.ftypeSubject.next(data);
    }

    updateInfoBarFType$(): Observable<string> {
        return this.ftypeSubject.asObservable();
    }

}