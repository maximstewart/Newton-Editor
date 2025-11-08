import {
    Component,
    ChangeDetectorRef,
    DestroyRef,
    ElementRef,
    HostBinding,
    ViewChild,
    inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { LspManagerService } from '../../common/services/editor/lsp-manager/lsp-manager.service';

import { CodeViewComponent } from '../code-view/view.component';

import { ServiceMessage } from '../../common/types/service-message.type';

import { ButtonMap } from '../../common/constants/button.map';



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
    readonly #destroyRef                           = inject(DestroyRef);
    private changeDetectorRef: ChangeDetectorRef   = inject(ChangeDetectorRef);

    lspManagerService: LspManagerService           = inject(LspManagerService);

    @HostBinding("class.hidden") isHidden: boolean = true;
    @ViewChild('lspEditorComponent') lspEditorComponent!: CodeViewComponent;
    @ViewChild('sessionEditorComponent') sessionEditorComponent!: CodeViewComponent;
    lspTextEditor: any;
    innerEditor: any;
    editor: any;
    activeFile: any;

    @ViewChild('contextMenu') contextMenu!: ElementRef;
    public showContextMenu: boolean = false;


    constructor() {
        this.loadSubscribers();
    }

    private ngAfterViewInit(): void {
        this.mapEditorsAndLoadConfig();
    }

    private mapEditorsAndLoadConfig() {
        this.lspTextEditor = this.lspEditorComponent.editor;
        this.innerEditor   = this.sessionEditorComponent.editor;

        this.lspTextEditor.on("input", () => {
            this.lspManagerService.lspConfigDataStr =
                this.lspTextEditor.session.getValue();
        });

        this.lspManagerService.loadLspConfigData().then((lspConfigData) => {
            this.lspTextEditor.session.setMode("ace/mode/json");
            this.lspTextEditor.session.setValue(lspConfigData);
        });
    }

    private loadSubscribers() {
        this.lspManagerService.getMessage$().pipe(
            takeUntilDestroyed(this.#destroyRef)
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

    protected handleActionMouseUp(event: any): void {
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

    public pasteText() {
        navigator.clipboard.readText().then((pasteText) => {
            if (pasteText.includes("\n") || !pasteText.startsWith("/")) return;
            this.lspManagerService.workspaceFolder = pasteText;
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

    public closeLanguageClient() {
        let mode = this.lspManagerService.getMode(this.editor.session);
        this.lspManagerService.closeLanguageProviderWithClientServer(mode);
    }

    public registerEditorToLanguageClient() {
        this.lspManagerService.registerEditorToLSPClient(this.editor);
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
        this.editor     = message.rawData.editor;
        this.activeFile = message.rawData.activeFile;

        // TODO: figure out why this doesn't update the session consistently...
        // It seems maybe bound to visible state as change detector ref didn't help either.
        // this.innerEditor.setSession(this.editor.session);
    }

    private editorUpdate(message: ServiceMessage) {
        if (
            !this.editor ||
            !message.rawData.activeFile
        ) return;

        this.editor.setSession(message.rawData.editor.getSession())
        this.activeFile = message.rawData.activeFile;

        this.lspManagerService.registerSession(this.editor);
    }

    private closeFile(message: ServiceMessage) {
        this.lspManagerService.closeDocument(message.rawData);
    }

}