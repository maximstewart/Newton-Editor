import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class WebsocketService {

    private socket$!: WebSocketSubject<any>;

    connect(url: string): Observable<any> {
        if (!this.socket$ || this.socket$.closed) {
            this.socket$ = webSocket(
                {
                    url,
                    deserializer: msg => msg.data
                }
            );
        }
        return this.socket$.asObservable();
    }

    send(message: any) {
        if (this.socket$) {
            this.socket$.next(message);
        }
    }

    close() {
        if (this.socket$) {
            this.socket$.complete();
        }
    }
}
