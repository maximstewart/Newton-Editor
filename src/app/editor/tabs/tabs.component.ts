import {
    Component,
    ChangeDetectorRef,
    DestroyRef,
    ElementRef,
    ViewChild,
    inject
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CdkDrag, CdkDragDrop, CdkDropList } from '@angular/cdk/drag-drop';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { TabsService } from '../../common/services/editor/tabs/tabs.service';

import { ServiceMessage } from '../../common/types/service-message.type';

import { ButtonMap } from '../../common/constants/button.map';



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

    @ViewChild('contextMenu') contextMenu!: ElementRef;
    public showContextMenu: boolean = false;

    tabs: any[] = this.tabsService.tabs;
    targetEvent!: any;
    activeTab!: any;


    constructor() {
        this.loadSubscribers();
    }


    private loadSubscribers() {
        this.tabsService.getMessage$().pipe(
            takeUntilDestroyed(this.#destroyRef)
        ).subscribe((message: ServiceMessage) => {
            let elm = document.querySelector(`[title="${message.filePath}"]`);

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
                case "highlight-active-tab":
                    console.log("\n\n")
                    console.log(message)
                    console.log(elm)
                    console.log(this.activeTab)

                    if (!elm) {
                        if (this.activeTab) {
                            this.activeTab.classList.remove("active-tab")
                            this.activeTab = elm;
                        }

                        break;
                    };

                    if (this.activeTab) {
                        if (
                            this.activeTab.getAttribute("title") == elm.getAttribute("title")
                        ) {
                            break;
                        }

                        this.activeTab.classList.remove("active-tab")
                    }

                    this.activeTab = elm;
                    elm.classList.add("active-tab");
                    elm.scrollIntoView(
                        {
                            behavior: "smooth",
                            block: "center",
                            inline: "center"
                        }
                    );

                    break;
                default:
                    break;
            }

        });
    }

    protected handleActionClick(event: any): void {
        if (ButtonMap.RIGHT === event.button) return;

        let target = event.target;

        this.showContextMenu = false;
        this.processTargetEvent(event);
    }

    protected handleActionMouseDown(event: any): void {
        if (ButtonMap.LEFT === event.button) return;

        let target = event.target;

        let menuElm = this.contextMenu.nativeElement;
        let pageX = event.clientX;
        let pageY = event.clientY;

        const origin = {
            left: pageX + 5,
            top: pageY - 5
        };

        menuElm.style.left   = `${origin.left}px`;
        menuElm.style.top    = `${origin.top}px`;
        this.targetEvent     = event;
        this.showContextMenu = true;
    }

    public hideContextMenu() {
        this.showContextMenu = false;
    }

    public contextMenuClicked(event: any) {
        this.showContextMenu = false;

        const command = event.target.getAttribute("command");
        const args    = event.target.getAttribute("args");

        if (!command) return;

        this[command]( (args) ? args : null );
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


    private close(event: any): void {
        this.tabsService.closeTab(
            this.targetEvent.srcElement.parentElement.getAttribute("title")
        );
    }

    private closeAll(event: any): void {
        let elm      = this.targetEvent.srcElement.parentElement;
        let startElm = elm;

        // clear right
        while (elm) {
            elm = elm.nextSibling;
            if (!elm || elm.nodeType == 8) continue;

            this.tabsService.closeTab( elm.getAttribute("title") );
        }

        // clear left
        elm = startElm;
        while (elm) {
            elm = elm.previousSibling;
            if (!elm || elm.nodeType == 8) continue;

            this.tabsService.closeTab( elm.getAttribute("title") );
        }

        // clear initial target
        elm = startElm;
        this.tabsService.closeTab( elm.getAttribute("title") );
    }

    private closeAllLeft(event: any): void {
        let elm = this.targetEvent.srcElement.parentElement;

        // clear left
        while (elm) {
            elm = elm.previousSibling;
            if (!elm || elm.nodeType == 8) continue;

            this.tabsService.closeTab( elm.getAttribute("title") );
        }
    }

    private closeAllRight(event: any): void {
        let elm = this.targetEvent.srcElement.parentElement;

        // clear right
        while (elm) {
            elm = elm.nextSibling;
            if (!elm || elm.nodeType == 8) continue;

            this.tabsService.closeTab( elm.getAttribute("title") );
        }
    }

    private processTargetEvent(event: any): void {
        let target = event.target;

        if ( target.classList.contains("tab") ) {
            let fpath = event.srcElement.getAttribute("title")
            this.tabsService.sendEditorsServiceAMessage("set-tab-to-editor", fpath);

            // this.updateActiveTabHighlight(fpath);
        } else if ( target.classList.contains("title") ) {
            let fpath = event.srcElement.parentElement.getAttribute("title")
            this.tabsService.sendEditorsServiceAMessage("set-tab-to-editor", fpath);
            // this.updateActiveTabHighlight(fpath);
        } else if ( target.classList.contains("close-button") ) {
            this.tabsService.closeTab(
                event.srcElement.parentElement.getAttribute("title")
            );
        }
    }

    private updateActiveTabHighlight(fpath: string): void {
        let message      = new ServiceMessage();
        message.action   = "highlight-active-tab";
        message.filePath = fpath;
        this.tabsService.sendMessage(message);
    }

}