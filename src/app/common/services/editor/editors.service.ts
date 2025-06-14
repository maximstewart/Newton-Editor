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
    private selectSessionLeftSubject: ReplaySubject<any>  = new ReplaySubject<any>(1);
    private selectSessionRightSubject: ReplaySubject<any> = new ReplaySubject<any>(1);
    private moveSessionLeftSubject: ReplaySubject<any>    = new ReplaySubject<any>(1);
    private moveSessionRightSubject: ReplaySubject<any>   = new ReplaySubject<any>(1);


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

    moveSessionLeft(data: string): void {
        this.moveSessionLeftSubject.next(data);
    }

    moveSessionLeftRequested$(): Observable<string> {
        return this.moveSessionLeftSubject.asObservable();
    }

    moveSessionRight(data: string): void {
        this.moveSessionRightSubject.next(data);
    }

    moveSessionRightRequested$(): Observable<string> {
        return this.moveSessionRightSubject.asObservable();
    }

    selectSessionLeft(data: string): void {
        this.selectSessionLeftSubject.next(data);
    }

    selectSessionLeftRequested$(): Observable<string> {
        return this.selectSessionLeftSubject.asObservable();
    }

    selectSessionRight(data: string): void {
        this.selectSessionRightSubject.next(data);
    }

    selectSessionRightRequested$(): Observable<string> {
        return this.selectSessionRightSubject.asObservable();
    }

}