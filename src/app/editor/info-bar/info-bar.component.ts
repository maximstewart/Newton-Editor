import { Component, DestroyRef, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

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
    readonly #destroyRef: DestroyRef       = inject(DestroyRef);

    private infoBarService: InfoBarService = inject(InfoBarService);

    fpath: string     = "";
    path: string      = "";
    cursorPos: string = "";
    encodeing: string = "";
    ftype: string     = "";


    constructor() {
        this.loadSubscribers();
    }


    private loadSubscribers() {
        this.infoBarService.updateInfoBarFPath$().pipe(
            takeUntilDestroyed(this.#destroyRef)
        ).subscribe((fpath: string) => {
            this.fpath = fpath;
            let _path  = fpath;

            if (fpath?.length > 67) {
                _path = "..." + fpath.slice(fpath.length - 67, fpath.length);
            }

            this.path = _path;
        });

        this.infoBarService.updateInfoBarCursorPos$().pipe(
            takeUntilDestroyed(this.#destroyRef)
        ).subscribe((cursorPos: any) => {
            this.cursorPos = `${cursorPos.row + 1}:${cursorPos.column}`;
        });

        this.infoBarService.updateInfoBarEncodeing$().pipe(
            takeUntilDestroyed(this.#destroyRef)
        ).subscribe((encodeing: string) => {
            this.encodeing = encodeing;
        });

        this.infoBarService.updateInfoBarFType$().pipe(
            takeUntilDestroyed(this.#destroyRef)
        ).subscribe((ftype: string) => {
            let mode   = ftype.split("/");
            this.ftype = mode[ mode.length - 1 ];
        });

    }


}