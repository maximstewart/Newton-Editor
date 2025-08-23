import { Injectable } from '@angular/core';
import { ReplaySubject, Observable } from 'rxjs';

import { ServiceMessage } from '../../../types/service-message.type';



@Injectable({
    providedIn: 'root'
})
export class MarkdownPreviewService {
    private messageSubject: ReplaySubject<ServiceMessage> = new ReplaySubject<ServiceMessage>(1);


    public sendMessage(data: ServiceMessage): void {
        this.messageSubject.next(data);
    }

    public getMessage$(): Observable<ServiceMessage> {
        return this.messageSubject.asObservable();
    }

}