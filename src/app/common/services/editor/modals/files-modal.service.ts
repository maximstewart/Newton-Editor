import { Injectable } from '@angular/core';
import { ReplaySubject, Observable } from 'rxjs';



@Injectable({
    providedIn: 'root'
})
export class FilesModalService {
    private showFilesModalSubject: ReplaySubject<null> = new ReplaySubject<null>(1);
    private addFileSubject: ReplaySubject<string>  = new ReplaySubject<string>(1);


    constructor() {
    }


    showFilesModal(): void {
        this.showFilesModalSubject.next(null);
    }

    showFilesModalRequested$(): Observable<null> {
        return this.showFilesModalSubject.asObservable();
    }

    addFileToModal(data: string): void {
        this.addFileSubject.next(data);
    }

    addFileToModalRequested$(): Observable<string> {
        return this.addFileSubject.asObservable();
    }

}