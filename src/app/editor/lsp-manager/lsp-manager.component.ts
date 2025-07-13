import { Component, ChangeDetectorRef, ElementRef, HostBinding, ViewChild, inject } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

import { LspManagerService } from '../../common/services/editor/lsp-manager/lsp-manager.service';

import { CodeViewComponent } from '../code-view/view.component';

import { ServiceMessage } from '../../common/types/service-message.type';



@Component({
    selector: 'lsp-manager',
    standalone: true,
    imports: [
        CodeViewComponent
    ],
    templateUrl: './lsp-manager.component.html',
    styleUrl: './lsp-manager.component.css',
    host: {
        'class': 'lsp-manager',
        "(keyup)": "globalLspManagerKeyHandler($event)"
    }
})
export class LspManagerComponent {
    private unsubscribe: Subject<void>            = new Subject();
    private changeDetectorRef: ChangeDetectorRef  = inject(ChangeDetectorRef);

    lspManagerService: LspManagerService           = inject(LspManagerService);

    @HostBinding("class.hidden") isHidden: boolean = true;
    @ViewChild('lspEditorComponent') lspEditorComponent!: CodeViewComponent;
    @ViewChild('sessionEditorComponent') sessionEditorComponent!: CodeViewComponent;
    lspTextEditor: any;
    innerEditor: any;
    editor: any;
    activeFile: any;




    constructor() {
    }


    private ngAfterViewInit(): void {
        this.mapEditorsAndLoadConfig();
        this.loadSubscribers();
    }

    private ngOnDestroy() {
        this.unsubscribe.next();
        this.unsubscribe.complete();
    }

    private mapEditorsAndLoadConfig() {
        this.lspTextEditor = this.lspEditorComponent.editor;
        this.innerEditor   = this.sessionEditorComponent.editor;

        this.lspManagerService.loadLspConfigData().then((lspConfigData) => {
            this.lspTextEditor.session.setMode("ace/mode/json");
            this.lspTextEditor.session.setValue(lspConfigData);
        });
    }

    private loadSubscribers() {
        this.lspManagerService.getMessage$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((message: ServiceMessage) => {
            if (message.action === "toggle-lsp-manager") {
                this.toggleLspManager(message);
            } else if (message.action === "set-active-editor") {
                this.setActiveEditor(message);
            } else if (message.action === "editor-update") {
                this.editorUpdate(message);
            } else if (message.action === "close-file") {
                this.closeFile(message);
            }
        });
    }

    public clearWorkspaceFolder() {
        this.lspManagerService.workspaceFolder = "";
    }

    public setWorkspaceFolder() {
        window.fs.chooseFolder().then((folder: string) => {
            if (!folder) return;

            this.lspManagerService.workspaceFolder = folder;
        });
    }

    public createLanguageClient() {
        let mode = this.lspManagerService.getMode(this.editor.session);
        this.lspManagerService.createLanguageProviderWithClientServer(mode);
    }

    public registerEditorToLanguageClient() {
        this.lspManagerService.registerEditorToLSPClient(this.editor);
/*
        this.lspManagerService.setSessionFilePath(
            this.editor.session,
            this.activeFile.path
        );
*/
    }


    public globalLspManagerKeyHandler(event: any) {
        if (event.ctrlKey && event.shiftKey && event.key === "l") {
            this.hideLspManager();
        }
    }

    public hideLspManager() {
        this.isHidden = true;
        this.editor.focus();
    }

    private toggleLspManager(message: ServiceMessage) {
        this.isHidden = !this.isHidden;

        if (this.isHidden) return;

        // Note: hack for issue with setActiveEditor TODO
        setTimeout(() => {
            this.innerEditor.setSession(this.editor.getSession());
        }, 10);
    }

    private setActiveEditor(message: ServiceMessage) {
        this.editor       = message.rawData.editor;
        this.activeFile   = message.rawData.activeFile;

        // TODO: figure out why this doesn't update the session consistently...
        // It seems maybe bound to visible state as change detector ref didn't help either.
        // this.innerEditor.setSession(this.editor.session);
    }

    private editorUpdate(message: ServiceMessage) {
        if (!message.rawData.activeFile) return;

        this.editor.setSession(message.rawData.editor.getSession())
        this.activeFile   = message.rawData.activeFile;

/*
        this.lspManagerService.setSessionFilePath(
            this.editor.session,
            this.activeFile.path
        );
*/

    }

    private closeFile(message: ServiceMessage) {
        this.lspManagerService.closeDocument(message.rawData);
    }

}