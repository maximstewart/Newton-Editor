import { Component, ElementRef, ViewChild, TemplateRef, ComponentRef, ViewContainerRef } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

import { NewtonEditorComponent } from "./newton-editor/newton-editor.component";
import { FilesModalComponent } from "./modals/files-modal.component";
import { EditorsService } from '../common/services/editor/editors.service';
import { TabsService } from '../common/services/editor/tabs/tabs.service';
import { FilesService } from '../common/services/editor/files.service';

import { DndDirective } from '../common/directives/dnd.directive';
import { NewtonFile } from '../common/types/file.type';
import { ServiceMessage } from '../common/types/service-message.type';



@Component({
    selector: 'editors',
    standalone: true,
    imports: [
        DndDirective,
        FilesModalComponent
    ],
    templateUrl: './editors.component.html',
    styleUrl: './editors.component.css',
    host: {
        'class': 'row'
    }
})
export class EditorsComponent {
    private unsubscribe = new Subject<void>();

    @ViewChild('containerRef', {read: ViewContainerRef}) containerRef!: ViewContainerRef;
    activeEditor!: string;


    constructor(
        private editorsService: EditorsService,
        private tabsService: TabsService,
        private filesService: FilesService
    ) {
    }


    public ngAfterViewInit(): void {
        this.loadSubscribers();
        this.loadMainSubscribers();

        let leftEditor                       = this.createEditor();
        let rightEditor                      = this.createEditor();

        this.activeEditor                    = leftEditor.instance.uuid;
        leftEditor.instance.isDefault        = true;
        leftEditor.instance.rightSiblingUUID = rightEditor.instance.uuid;
        rightEditor.instance.leftSiblingUUID = leftEditor.instance.uuid;
    }

    loadSubscribers() {

        this.editorsService.getMessage$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((message: ServiceMessage) => {
            if (message.action === "select-left-editor") {
                let editorComponent  = this.editorsService.get(message.editorUUID);
                if (!editorComponent.leftSiblingUUID) return;
                let siblingComponent = this.editorsService.get(editorComponent.leftSiblingUUID);
                siblingComponent.editor.focus()
            } else if (message.action === "select-right-editor") {
                let editorComponent  = this.editorsService.get(message.editorUUID);
                if (!editorComponent.rightSiblingUUID) return;
                let siblingComponent = this.editorsService.get(editorComponent.rightSiblingUUID);
                siblingComponent.editor.focus()
            } else if (message.action === "move-session-left") {
                let editorComponent  = this.editorsService.get(message.editorUUID);
                if (!editorComponent.leftSiblingUUID) return;
                let siblingComponent = this.editorsService.get(editorComponent.leftSiblingUUID);
                let session = editorComponent.editor.getSession();
                let siblingSession = siblingComponent.editor.getSession();

                if (session == siblingSession) return;
                siblingComponent.editor.setSession(session);
                editorComponent.newBuffer();
                siblingComponent.editor.focus()
            } else if (message.action === "move-session-right") {
                let editorComponent  = this.editorsService.get(message.editorUUID);
                if (!editorComponent.rightSiblingUUID) return;
                let siblingComponent = this.editorsService.get(editorComponent.rightSiblingUUID);
                let session = editorComponent.editor.getSession();
                let siblingSession = siblingComponent.editor.getSession();

                if (session == siblingSession) return;
                siblingComponent.editor.setSession(session);
                editorComponent.newBuffer();
                siblingComponent.editor.focus()
            } else if (message.action === "set-active-editor") {
                this.editorsService.get(this.activeEditor).removeActiveStyling();
                this.activeEditor = message.editorUUID;
                this.editorsService.get(this.activeEditor).addActiveStyling();
            } else if (message.action === "set-tab-to-editor") {
                let file            = this.filesService.get(message.filePath);
                let editorComponent = this.getActiveEditorComponent();
                let editor          = editorComponent.editor;

                editorComponent.activeFile = file;
                editor.setSession(file.session);
            } else if (message.action === "close-tab") {
                let file    = this.filesService.get(message.filePath);
                let editors = this.editorsService.getEditorsAsArray();

                for (let i = 0; i < editors.length; i++) {
                    let editorComponent = editors[i].instance;
                    if (editorComponent.editor.session == file.session) {
                        editorComponent.newBuffer();
                    }
                }

                this.filesService.delete(file);
            }

        });

    }

    loadMainSubscribers() {
        window.fs.onLoadFiles(async (paths: []) => {
            for (let i = 0; i < paths.length; i++) {
                let file = new File([], "") as NewtonFile;

                if ( this.filesService.get(paths[i]) ) continue;

                await this.filesService.addFile(paths[i], file);
                this.filesService.addTab(file);
            }

            let path = paths[ paths.length - 1 ];
            let file = this.filesService.get(path);
            this.setSession(file);
        });

        window.fs.onChangedFile(async (path: string) => {
            let message      = new ServiceMessage();
            message.action   = "file-changed";
            message.filePath = path;
            this.tabsService.sendMessage(message);
        });

        window.fs.onDeletedFile(async (path: string) => {
            let message      = new ServiceMessage();
            message.action   = "file-deleted";
            message.filePath = path;

            this.tabsService.sendMessage(message);
            this.filesService.sendMessage(message);
        });

        window.fs.onSavedFile(async (path: string) => {
            let message      = new ServiceMessage();
            message.action   = "file-saved";
            message.filePath = path;

            this.tabsService.sendMessage(message);
        });

        window.fs.onUpdateFilePath(async (path: string) => {
            console.log(path);
            // this.tabsService.sendMessage(message);
            // this.filesService.sendMessage(message);
        });

        window.main.onMenuActions(async (action: string) => {
            let editorComponent = this.getActiveEditorComponent();
            let editor          = editorComponent.editor;

            switch ( action ) {
                case "new-file":
                    break;
                case "open-files":
                    editorComponent.openFiles();
                    break;
                case "save-file":
                    editorComponent.saveFile();
                    break;
                case "save-file-as":
                    editorComponent.saveFileAs();
                    break;
                case "cut":
                    editorComponent.cutText();
                    break;
                case "copy":
                    editorComponent.copyText();
                   break;
                case "paste":
                    editorComponent.pasteText();
                    break;
                case "zoom-in":
                    editorComponent.zoomIn()
                    break;
                case "zoom-out":
                    editorComponent.zoomOut()
                    break;
                case "open-settings":
                    editor.showSettingsMenu();
                case "show-about":
                    break;
                default:
                    editor.execCommand(action);
            }
        });
    }

    ngOnDestroy() {
        this.unsubscribe.next();
        this.unsubscribe.complete();
    }

    // Note: Only really works with 2 editors and very brittle logic.
    protected setEditorSize(event: any) {
        let lEditorComponent = null;
        let rEditorComponent = null;
        let lSize = 6;
        let rSize = 6;

        if (
            event.target.parentElement.classList.contains("editor-left-size")
        ) {
            lSize   = parseInt(
                event.target.classList[1].split("-")[1]
            );
            rSize   = 12 - lSize;

            lEditorComponent = this.editorsService.get(this.activeEditor);
            if (lEditorComponent.leftSiblingUUID) {
                rEditorComponent = lEditorComponent;
                lEditorComponent = this.editorsService.get(lEditorComponent.leftSiblingUUID);
            } else {
                rEditorComponent = this.editorsService.get(lEditorComponent.rightSiblingUUID);
            }
        } else {
            rSize   = parseInt(
                event.target.classList[1].split("-")[1]
            );
            lSize   = 12 - rSize;
            rEditorComponent = this.editorsService.get(this.activeEditor);
            if (rEditorComponent.rightSiblingUUID) {
                lEditorComponent = rEditorComponent;
                rEditorComponent = this.editorsService.get(rEditorComponent.rightSiblingUUID);
            } else {
                lEditorComponent = this.editorsService.get(rEditorComponent.leftSiblingUUID);
            }
        }

        let lElm = lEditorComponent.editorElm.nativeElement.parentElement;
        let rElm = rEditorComponent.editorElm.nativeElement.parentElement;

        lElm.setAttribute(
            'class',
            (lSize == 0) ? "hidden" : `col col-${lSize}`
        );

        rElm.setAttribute(
            'class',
            (rSize == 0) ? "hidden" : `col col-${rSize}`
        );

        if (lSize == 0) rEditorComponent.editor.focus();
        if (rSize == 0) lEditorComponent.editor.focus();
    }

    private createEditor() {
        const component = this.containerRef.createComponent(NewtonEditorComponent);
        component.instance.editorSettings = this.editorsService.editorSettings;
        this.editorsService.set(component.instance.uuid, component)

        return component;
    }

    protected onFileDropped(files: any) {
        this.filesService.loadFilesList(files).then((file: NewtonFile | undefined | null) => {
            this.setSession(file);
        });
    }

    private async setSession(file: NewtonFile | undefined | null) {
        if ( !file ) return;
        let editorComponent        = this.getActiveEditorComponent();
        let editor                 = editorComponent.editor;

        editorComponent.activeFile = file;
        editor.setSession(file.session);
    }

    private getSession() {
        let editorComponent = this.editorsService.get(this.activeEditor);
        let editor          = editorComponent.editor;

        return editor.getSession();
    }

    private getActiveEditorComponent(): any {
        return this.editorsService.get(this.activeEditor);
    }

    private getActiveEditor(): any {
        let editorComponent = this.editorsService.get(this.activeEditor);
        let editor          = editorComponent.editor;
        return editor;
    }

}