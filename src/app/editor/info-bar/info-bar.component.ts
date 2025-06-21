import { Component, inject } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

import { InfoBarService } from '../../common/services/editor/info-bar/info-bar.service';



@Component({
    selector: 'info-bar',
    standalone: true,
    imports: [
    ],
    templateUrl: './info-bar.component.html',
    styleUrl: './info-bar.component.css',
    host: {
        'class': 'row info-bar'
    }
})
export class InfoBarComponent {
    private unsubscribe: Subject<void>     = new Subject();

    private infoBarService: InfoBarService = inject(InfoBarService);

    fpath: string     = "";
    path: string      = "";
    cursorPos: string = "";
    encodeing: string = "";
    ftype: string     = "";


    constructor() {}


    public ngAfterViewInit(): void {
        this.loadSubscribers();
    }


    loadSubscribers() {

        this.infoBarService.updateInfoBarFPath$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((fpath: string) => {
            this.fpath = fpath;
            let _path  = fpath;

            if (fpath?.length > 67) {
                _path = "..." + fpath.slice(fpath.length - 67, fpath.length);
            }

            this.path = _path;
        });

        this.infoBarService.updateInfoBarCursorPos$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((cursorPos: any) => {
            this.cursorPos = `${cursorPos.row + 1}:${cursorPos.column}`;
        });

        this.infoBarService.updateInfoBarEncodeing$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((encodeing: string) => {
            this.encodeing = encodeing;
        });

        this.infoBarService.updateInfoBarFType$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((ftype: string) => {
            let mode   = ftype.split("/");
            this.ftype = mode[ mode.length - 1 ];
        });

    }


}