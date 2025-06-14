import { Component, ElementRef, ViewChild, TemplateRef, ComponentRef, ViewContainerRef } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

import { NewtonEditorComponent } from "./newton-editor/newton-editor.component";
import { EditorsService } from '../common/services/editor/editors.service';
import { FilesService } from '../common/services/editor/files.service';

import { DndDirective } from '../common/directives/dnd.directive';
import { NewtonFile } from '../common/types/file.type';
import { ServiceMessage } from '../common/types/service-message.type';



@Component({
    selector: 'editors',
    standalone: true,
    imports: [
        DndDirective
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

        this.editorsService.selectSessionLeftRequested$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((uuid: string) => {
            let editorComponent  = this.editorsService.get(uuid);
            if (!editorComponent.leftSiblingUUID) return;
            let siblingComponent = this.editorsService.get(editorComponent.leftSiblingUUID);
            siblingComponent.editor.focus()
        });

        this.editorsService.selectSessionRightRequested$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((uuid: string) => {
            let editorComponent  = this.editorsService.get(uuid);
            if (!editorComponent.rightSiblingUUID) return;
            let siblingComponent = this.editorsService.get(editorComponent.rightSiblingUUID);
            siblingComponent.editor.focus()
        });

        this.editorsService.moveSessionLeftRequested$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((uuid: string) => {
            let editorComponent  = this.editorsService.get(uuid);
            if (!editorComponent.leftSiblingUUID) return;
            let siblingComponent = this.editorsService.get(editorComponent.leftSiblingUUID);
            let session = editorComponent.editor.getSession();
            let siblingSession = siblingComponent.editor.getSession();

            if (session == siblingSession) return;
            siblingComponent.editor.setSession(session);
            editorComponent.newBuffer();
            siblingComponent.editor.focus()
        });

        this.editorsService.moveSessionRightRequested$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((uuid: string) => {
            let editorComponent  = this.editorsService.get(uuid);
            if (!editorComponent.rightSiblingUUID) return;
            let siblingComponent = this.editorsService.get(editorComponent.rightSiblingUUID);
            let session = editorComponent.editor.getSession();
            let siblingSession = siblingComponent.editor.getSession();

            if (session == siblingSession) return;
            siblingComponent.editor.setSession(session);
            editorComponent.newBuffer();
            siblingComponent.editor.focus()
        });

        this.editorsService.newActiveEditor$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((uuid: string) => {
            this.editorsService.get(this.activeEditor).removeActiveStyling();
            this.activeEditor = uuid;
            this.editorsService.get(this.activeEditor).addActiveStyling();
        });

        this.editorsService.loadTabToEditor$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((path: string) => {
            let file            = this.filesService.get(path);
            let editorComponent = this.getActiveEditorComponent();
            let editor          = editorComponent.editor;

            editorComponent.activeFile = file;
            editor.setSession(file.session);
        });

        this.editorsService.closeTabRequested$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((path: string) => {
            let file    = this.filesService.get(path);
            let editors = this.editorsService.getEditorsAsArray();

            for (let i = 0; i < editors.length; i++) {
                let editorComponent = editors[i].instance;
                if (editorComponent.editor.session == file.session) {
                    editorComponent.newBuffer();
                }
            }

            this.filesService.delete(file);
        });

    }

    loadMainSubscribers() {
        window.fs.onLoadFiles(async (paths: []) => {
            for (let i = 0; i < paths.length; i++) {
                let file = new File([], "") as NewtonFile;

                await this.filesService.addFile(paths[i], file);
                this.filesService.addTab(file);
            }

            let path = paths[ paths.length - 1 ];
            let file = this.filesService.get(path);
            this.setSession(file);
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