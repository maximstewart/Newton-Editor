import { Injectable } from '@angular/core';
import { BehaviorSubject, ReplaySubject, Observable } from 'rxjs';

import { ServiceMessage } from '../../../types/service-message.type';


@Injectable({
    providedIn: 'root'
})
export class TabsService {
    private messageSubject: ReplaySubject<ServiceMessage> = new ReplaySubject<ServiceMessage>(1);

    constructor() {}


    sendMessage(data: ServiceMessage): void {
        this.messageSubject.next(data);
    }

    getMessage$(): Observable<ServiceMessage> {
        return this.messageSubject.asObservable();
    }
}