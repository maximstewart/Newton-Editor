import { Component, inject } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

import { EditorsService } from '../common/services/editor/editors.service';
import { TabsService } from '../common/services/editor/tabs/tabs.service';
import { FilesService } from '../common/services/files.service';

import { CodeViewComponent } from "./code-view/view.component";

import { DndDirective } from '../common/directives/dnd.directive';
import { PaneHandleDirective } from '../common/directives/pane-handle.directive';
import { NewtonFile } from '../common/types/file.type';
import { ServiceMessage } from '../common/types/service-message.type';



@Component({
    selector: 'editors',
    standalone: true,
    imports: [
        DndDirective,
        PaneHandleDirective,
        CodeViewComponent
    ],
    templateUrl: './editors.component.html',
    styleUrl: './editors.component.css',
    host: {
        'class': 'row'
    }
})
export class EditorsComponent {
    private unsubscribe: Subject<void>     = new Subject();

    private editorsService: EditorsService = inject(EditorsService);
    private tabsService: TabsService       = inject(TabsService);
    private filesService: FilesService     = inject(FilesService);


    constructor() {
    }


    private ngAfterViewInit(): void {
        this.loadSubscribers();
        this.loadMainSubscribers();
    }

    private ngOnDestroy() {
        this.unsubscribe.next();
        this.unsubscribe.complete();
    }

    private loadSubscribers() {

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

                siblingComponent.assignSession(editorComponent.activeFile);

                let targetPath = this.tabsService.getRightSiblingTab(
                    editorComponent.activeFile.path
                )
                if (targetPath) {
                    editorComponent.assignSession(
                        this.filesService.get(targetPath)
                    );
                } else {
                    editorComponent.newFile();
                }

                siblingComponent.editor.focus()
            } else if (message.action === "move-session-right") {
                let editorComponent  = this.editorsService.get(message.editorUUID);
                if (!editorComponent.rightSiblingUUID) return;

                let siblingComponent = this.editorsService.get(editorComponent.rightSiblingUUID);
                let session = editorComponent.editor.getSession();
                let siblingSession = siblingComponent.editor.getSession();

                if (session == siblingSession) return;

                siblingComponent.assignSession(editorComponent.activeFile);

                let targetPath = this.tabsService.getRightSiblingTab(
                    editorComponent.activeFile.path
                )
                if (targetPath) {
                    editorComponent.assignSession(
                        this.filesService.get(targetPath)
                    );
                } else {
                    editorComponent.newFile();
                }

                siblingComponent.editor.focus()
            } else if (message.action === "set-active-editor") {
                this.editorsService.getActiveEditorComponent().removeActiveStyling();
                this.editorsService.setActiveEditor(message.editorUUID);
                this.editorsService.getActiveEditorComponent().addActiveStyling();
            } else if (message.action === "set-tab-to-editor") {
                let file            = this.filesService.get(message.filePath);
                let editorComponent = this.editorsService.getActiveEditorComponent();
                let editor          = editorComponent.editor;

                editorComponent.assignSession(file);
                this.editorsService.miniMapView.cloneSession(file);
            } else if (message.action === "close-tab") {
                let activeComponent = this.editorsService.getActiveEditorComponent();
                let editors         = this.editorsService.getEditorsAsArray();
                let file            = this.filesService.get(message.filePath);

                for (let i = 0; i < editors.length; i++) {
                    let editorComponent = editors[i];

                    if (editorComponent.editor.session !== file.session) continue;

                    let targetFile = this.filesService.getPreviousFile(file.path)
                    if (targetFile) {
                        editorComponent.assignSession(targetFile);
                        if (activeComponent == editorComponent) {
                            this.editorsService.miniMapView.cloneSession(targetFile);
                        }
                    } else {
                        editorComponent.newFile();
                        if (activeComponent == editorComponent) {
                            this.editorsService.miniMapView.newFile();
                        }
                    }

                }

                activeComponent.lspManagerService.closeDocument(file.session);
                this.filesService.unset(file);
            }

        });

    }

    private loadMainSubscribers() {
        window.fs.onLoadFiles(async (paths: []) => {
            for (let i = 0; i < paths.length; i++) {
                let file = new File([], "") as NewtonFile;

                if ( this.filesService.get(paths[i]) ) continue;

                await this.filesService.addFile(paths[i], file);
                this.filesService.addTab(file);
            }

            let path = paths[ paths.length - 1 ];
            let file = this.filesService.get(path);
            this.editorsService.setSession(file);
        });

        window.fs.onChangedFile(async (path: string, data: string) => {
            let file = this.filesService.get(path);
            file.session.setValue(data);

            // Note: fake 'save' event to not show as changed iven external save happened...
            let message      = new ServiceMessage();
            message.action   = "file-saved";
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
            console.log("TODO (onUpdateFilePath) :", path);
            // this.tabsService.sendMessage(message);
            // this.filesService.sendMessage(message);
        });

        window.main.onMenuActions(async (action: string) => {
            let editorComponent = this.editorsService.getActiveEditorComponent();
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
                case "quit":
                    window.main.quit();
                    break;
                default:
                    editor.execCommand(action);
            }
        });
    }

    protected onFileDropped(files: any) {
        this.filesService.loadFilesList(files).then((file: NewtonFile | undefined | null) => {
            // Note: if we drop an already loaded file the path doesn't get set and
            // therefor the last file in drop list might get returned without path.
            if (!file.path) return;

            this.editorsService.setSession(file);
        });
    }

}