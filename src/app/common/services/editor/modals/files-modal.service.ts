import { Injectable } from '@angular/core';
import { ReplaySubject, Observable } from 'rxjs';



@Injectable({
    providedIn: 'root'
})
export class FilesModalService {
    private showFilesModalSubject: ReplaySubject<null> = new ReplaySubject<null>(1);
    private addFileSubject: ReplaySubject<string>      = new ReplaySubject<string>(1);


    public showFilesModal(): void {
        this.showFilesModalSubject.next(null);
    }

    public showFilesModalRequested$(): Observable<null> {
        return this.showFilesModalSubject.asObservable();
    }

    public addFileToModal(data: string): void {
        this.addFileSubject.next(data);
    }

    public addFileToModalRequested$(): Observable<string> {
        return this.addFileSubject.asObservable();
    }

}