import { Component, ElementRef, ViewChild, TemplateRef, ComponentRef, ViewContainerRef } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

import { EditSession } from 'ace-builds';
import { getModeForPath } from 'ace-builds/src-noconflict/ext-modelist';

import { AceEditorComponent } from "./ace/ace-editor.component";
import { EditorsService } from '../common/services/editor/editors.service';
import { TabsService } from '../common/services/editor/tabs/tabs.service';

import { DndDirective } from '../common/directives/dnd.directive';
import { NewtonFile } from '../common/types/file.type';
import { ServiceMessage } from '../common/types/service-message.type';
import { EditorSettings } from "../common/configs/editor.config";



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
    editors: Map<string, ComponentRef<AceEditorComponent>>;
    editorSettings: typeof EditorSettings;
    files: Map<string, NewtonFile>;
    activeEditor!: string;
    lspConfigData!: any;


    constructor(
        private editorsService: EditorsService,
        private tabsService: TabsService
    ) {
        this.editorSettings = EditorSettings;
        this.editors = new Map<string, ComponentRef<AceEditorComponent>>();
        this.files   = new Map<string, NewtonFile>();
    }


    public ngAfterViewInit(): void {
        this.loadSubscribers();
        this.loadMainSubscribers();

        let editor                = this.createEditor();
        this.activeEditor         = editor.instance.uuid;
        editor.instance.isDefault = true;

        this.createEditor();
    }

    loadSubscribers() {
        this.editorsService.newActiveEditor$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((uuid: string) => {
            this.editors.get(this.activeEditor).instance.removeActiveStyling();
            this.activeEditor = uuid;
            this.editors.get(this.activeEditor).instance.addActiveStyling();
        });

        this.editorsService.loadTabToEditor$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((path: string) => {
            let file            = this.files.get(path);
            let editorComponent = this.getActiveEditorComponent();
            let editor          = editorComponent.editor;

            editorComponent.activeFile = file;
            editor.setSession(file.session);
        });

        this.editorsService.closeTabRequested$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((path: string) => {
            let file    = this.files.get(path);
            let editors = [...this.editors.values()];

            for (let i = 0; i < editors.length; i++) {
                let editorComponent = editors[i].instance;
                if (editorComponent.editor.session == file.session) {
                    editorComponent.newBuffer();
                }
            }

            file.session.destroy();
            this.files.delete(path);
        });
    }

    loadMainSubscribers() {
        window.fs.onLoadFiles(async (paths: []) => {
            for (let i = 0; i < paths.length; i++) {
                let file = new File([], "") as NewtonFile;

                await this.addFile(paths[i], file);
                this.addTab(file);
            }

            let file = this.files.get(paths[ paths.length - 1 ]);
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

    private createEditor() {
        const component = this.containerRef.createComponent(AceEditorComponent);
        component.instance.editorSettings = this.editorSettings;
        this.editors.set(component.instance.uuid, component)

        return component;
    }

    protected onFileDropped(files: any) {
        this.loadFilesList(files).then((file: NewtonFile | undefined | null) => {
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
        let editorComponent = this.editors.get(this.activeEditor)?.instance;
        let editor          = editorComponent.editor;

        return editor.getSession();
    }

    private getActiveEditorComponent(): any {
        return this.editors.get(this.activeEditor)?.instance;
    }

    private getActiveEditor(): any {
        let editorComponent = this.editors.get(this.activeEditor)?.instance;
        let editor          = editorComponent.editor;
        return editor;
    }

    private async loadFilesList(files: Array<NewtonFile>): Promise<NewtonFile | undefined | null> {
	    for (let i = 0; i < files.length; i++) {
		    const file = files[i];
		    const path = window.fs.getPathForFile(file);

		    if (!file || !path) continue;
		    if ( this.files.get(path) ) continue;

		    await this.addFile(path, file);
		    this.addTab(file);
	    }

	    return files[ files.length - 1 ];
    }

    private async addFile(path: string, file: NewtonFile): Promise<void> {
	    try {
	        let pathParts = path.split("/");
	        file.fname    = pathParts[ pathParts.length - 1 ];
	        file.path     = path;
	        file.hash     = btoa(file.path);
	        let data      = await window.fs.getFileContents(file.path);
            file.session  = new EditSession(data);

            file.session.setMode(
                getModeForPath( file.path ).mode
            );

            this.files.set(file.path, file);
	    } catch (error) {
		    console.log(
		        `----  Error  ----\nPath: ${path}\nMessage: ${error}`
		    );
	    }
    }

    private async addTab(file: NewtonFile) {
        let message     = new ServiceMessage();
        message.action  = "create-tab";
        message.message = file.fname;
        message.uuid    = file.hash;
        message.data    = file.path;

        this.tabsService.setData(message);
    }

}