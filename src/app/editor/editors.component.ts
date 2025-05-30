import { Component, ElementRef, ViewChild, TemplateRef, ComponentRef, ViewContainerRef } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import * as uuid from 'uuid';

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

        let editor = this.createEditor();
        this.activeEditor = editor.instance.uuid;
        this.createEditor();
    }

    loadSubscribers() {
        this.editorsService.newActiveEditor$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((uuid: string) => {
            this.activeEditor = uuid;
        });
    }

    ngOnDestroy() {
        this.unsubscribe.next();
        this.unsubscribe.complete();
    }

    private createEditor() {
        const component = this.containerRef.createComponent(AceEditorComponent);
        component.instance.editorSettings = this.editorSettings;
        component.instance.uuid = uuid.v4();
        this.editors.set(component.instance.uuid, component)

        return component;
    }

    protected onFileDropped(event: any) {
        this.loadFilesList(event).then((session: EditSession | undefined | null) => {
	        if ( !session ) return;

	        let editorComponent = this.editors.get(this.activeEditor)?.instance;
	        let editor = editorComponent.editor;
	        editor?.setSession(session);
	        editorComponent.registerEditorToLSPMode();
        });
    }

    private async loadFilesList(files: Array<NewtonFile>): Promise<EditSession | undefined | null> {
	    for (let i = 0; i < files.length; i++) {
		    const file = files[i];
		    const path = window.fs.getPathForFile(file);

		    if (!file || !path) continue;
		    if ( this.files.get(path) ) continue;
		    
		    await this.addFile(path, file);
		    this.addTab(file);
	    }

	    return files[ files.length - 1 ].session;
    }

    private async addFile(path: string, file: NewtonFile) {
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

        this.tabsService.setData(message);
    }

}