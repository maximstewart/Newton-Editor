import { Component, ElementRef, HostBinding, ViewChild, inject } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

import { LspManagerService } from '../../common/services/editor/lsp-manager/lsp-manager.service';

import { ServiceMessage } from '../../common/types/service-message.type';



@Component({
    selector: 'lsp-manager',
    standalone: true,
    imports: [
    ],
    templateUrl: './lsp-manager.component.html',
    styleUrl: './lsp-manager.component.css',
    host: {
        'class': 'lsp-manager',
        "(keyup)": "globalLspManagerKeyHandler($event)"
    }
})
export class LspManagerComponent {
    private unsubscribe: Subject<void>             = new Subject();

    private lspManagerService: LspManagerService   = inject(LspManagerService);

    @HostBinding("class.hidden") isHidden: boolean = true;
    @ViewChild('lspConfigText') lspConfigText!: ElementRef;
    private editors: any                           = {}; 
    private editor: any; 


    constructor() {
    }


    private ngAfterViewInit(): void {
        this.lspConfigText.nativeElement.value = this.lspManagerService.lspConfigData;

        this.loadSubscribers();
    }

    private ngOnDestroy() {
        this.unsubscribe.next();
        this.unsubscribe.complete();
    }

    private loadSubscribers() {
        this.lspManagerService.getMessage$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((message: ServiceMessage) => {
            if (message.action === "toggle-lsp-manager") {
                this.toggleLspManager(message);
            } else if (message.action === "set-active-editor") {
                this.setActiveEditor(message);
            } else if (message.action === "register-editor") {
                this.registerEditor(message);
            }
        });
    }

    public hideLspManager() {
        this.isHidden = true;
        this.editor.focus();
    }

    public globalLspManagerKeyHandler(event: any) {
        if (event.ctrlKey && event.shiftKey && event.key === "l") {
            this.hideLspManager();
        }
    }


    private toggleLspManager(message: ServiceMessage) {
        this.isHidden = !this.isHidden;
    }

    private setActiveEditor(message: ServiceMessage) {
        this.editor = this.editors[message.editorUUID];
    }

    private registerEditor(message: ServiceMessage) {
        let _editor = message.rawData;
        this.editors[_editor.uuid] = _editor.editor;
    }

}