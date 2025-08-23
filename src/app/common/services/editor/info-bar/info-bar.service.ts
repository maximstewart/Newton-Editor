import { Injectable } from '@angular/core';
import { BehaviorSubject, ReplaySubject, Observable } from 'rxjs';

import { ServiceMessage } from '../../../types/service-message.type';


@Injectable({
    providedIn: 'root'
})
export class InfoBarService {
    private dataSubject: ReplaySubject<ServiceMessage> = new ReplaySubject(1);
    private fpathSubject: ReplaySubject<string>        = new ReplaySubject(1);
    private cursorPosSubject: ReplaySubject<any>       = new ReplaySubject(1);
    private encodeingSubject: ReplaySubject<string>    = new ReplaySubject(1);
    private ftypeSubject: ReplaySubject<string>        = new ReplaySubject(1);


    public setData(data: ServiceMessage): void {
        this.dataSubject.next(data);
    }

    public getData$(): Observable<ServiceMessage> {
        return this.dataSubject.asObservable();
    }

    public setInfoBarFPath(data: string): void {
        this.fpathSubject.next(data);
    }

    public updateInfoBarFPath$(): Observable<string> {
        return this.fpathSubject.asObservable();
    }

    public setInfoBarCursorPos(data: any): void {
        this.cursorPosSubject.next(data);
    }

    public updateInfoBarCursorPos$(): Observable<any> {
        return this.cursorPosSubject.asObservable();
    }

    public setInfoBarEncodeing(data: string): void {
        this.encodeingSubject.next(data);
    }

    public updateInfoBarEncodeing$(): Observable<string> {
        return this.encodeingSubject.asObservable();
    }

   public setInfoBarFType(data: string): void {
        this.ftypeSubject.next(data);
    }

    public updateInfoBarFType$(): Observable<string> {
        return this.ftypeSubject.asObservable();
    }

}