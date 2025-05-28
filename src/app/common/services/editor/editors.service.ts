import { Injectable } from '@angular/core';
import { BehaviorSubject, ReplaySubject, Observable } from 'rxjs';

import { ServiceMessage } from '../../types/service-message.type';


@Injectable({
    providedIn: 'root'
})
export class EditorsService {
    private dataSubject: ReplaySubject<ServiceMessage> = new ReplaySubject<ServiceMessage>(1);

    constructor() {}

    setData(data: ServiceMessage): void {
        this.dataSubject.next(data);
    }

    getData$(): Observable<ServiceMessage> {
        return this.dataSubject.asObservable();
    }
}