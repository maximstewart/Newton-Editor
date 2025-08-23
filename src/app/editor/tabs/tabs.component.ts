import {
    Component,
    ChangeDetectorRef,
    DestroyRef,
    inject
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CdkDrag, CdkDragDrop, CdkDropList } from '@angular/cdk/drag-drop';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { TabsService } from '../../common/services/editor/tabs/tabs.service';

import { ServiceMessage } from '../../common/types/service-message.type';



@Component({
    selector: 'tabs',
    standalone: true,
    imports: [
        CommonModule,
        CdkDropList,
        CdkDrag,
    ],
    templateUrl: './tabs.component.html',
    styleUrl: './tabs.component.css',
    host: {
        'class': 'tabs scroller'
    }
})
export class TabsComponent {
    readonly #destroyRef                         = inject(DestroyRef);

    private tabsService: TabsService             = inject(TabsService);
    private changeDetectorRef: ChangeDetectorRef = inject(ChangeDetectorRef);

    tabs: any[] = this.tabsService.tabs;


    constructor() {
        this.loadSubscribers();
    }


    private loadSubscribers() {
        this.tabsService.getMessage$().pipe(
            takeUntilDestroyed(this.#destroyRef)
        ).subscribe((message: ServiceMessage) => {
            let elm = document.querySelectorAll(`[title="${message.filePath}"]`)[1];

            switch ( message.action ) {
                case "create-tab":
                    this.createTab(message.fileName, message.fileUUID, message.filePath);
                    break;
                case "file-changed":
                    elm.classList.add("file-changed");
                    elm.classList.remove("file-deleted");
                    break;
                case "file-deleted":
                    elm.classList.add("file-deleted");
                    elm.classList.remove("file-changed");
                    break;
                case "file-saved":
                    elm.classList.remove("file-deleted");
                    elm.classList.remove("file-changed");
                    break;
                default:
                    break;
            }

        });
    }

    protected handleAction(event: any): void {
        let target = event.target;

        if ( target.classList.contains("tab") ) {
            this.tabsService.sendEditorsServiceAMessage(
                "set-tab-to-editor",
                event.srcElement.getAttribute("title")
            );

        } else if ( target.classList.contains("title") ) {
            this.tabsService.sendEditorsServiceAMessage(
                "set-tab-to-editor",
                event.srcElement.parentElement.getAttribute("title")
            );
        } else if ( target.classList.contains("close-button") ) {
            this.tabsService.closeTab(
                event.srcElement.parentElement.getAttribute("title")
            );
        }

    }

    public createTab(title: string, uuid: string, path: string): void {
        this.tabsService.push({title: title, uuid: uuid, path: path});
        this.changeDetectorRef.detectChanges();
    }

    private moved(event: any): void {
        let target = event.event.target;
        let fpath  = "";

        if ( target.classList.contains("title") ||
            target.classList.contains("close-button")
        ) {
            fpath = target.parentElement.getAttribute("title")
        } else (
            fpath = target.getAttribute("title")
        )

        this.tabsService.setNewTargetIndex(fpath);
    }

    protected dropped(event: CdkDragDrop<any>): void {
        this.tabsService.move(event.previousIndex);
    }

}