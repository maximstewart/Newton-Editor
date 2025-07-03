import { Injectable } from '@angular/core';
import { ReplaySubject, Observable } from 'rxjs';

import { CodeViewComponent } from "../../../editor/code-view/view.component";

import { ServiceMessage } from '../../types/service-message.type';
import { EditorSettings } from "../../configs/editor.config";

import { NewtonFile } from '../../types/file.type';



@Injectable({
    providedIn: 'root'
})
export class EditorsService {
    private messageSubject: ReplaySubject<ServiceMessage> = new ReplaySubject<ServiceMessage>(1);

    editors: Map<string, CodeViewComponent>;
    editorSettings: typeof EditorSettings;

    activeEditor!: string;
    miniMapView!: CodeViewComponent;


    constructor() {
        this.editorSettings = EditorSettings;
        this.editors = new Map<string, CodeViewComponent>();
    }


    public getEditorsAsArray(): CodeViewComponent[] {
        return [...this.editors.values()];
    }

    public get(uuid: string): CodeViewComponent {
        return this.editors.get(uuid);
    }

    public set(uuid: string, component: CodeViewComponent) {
        if (component.isMiniMap) {
            this.miniMapView = component;
            return;
        }

        this.editors.set(uuid, component);

        if (Array.from(this.editors.keys()).length <= 1) return;

        let _editors    = this.getEditorsAsArray();
        let leftEditor  = null;
        let rightEditor = null;

        for (let i = 0; i < _editors.length; i++) {
            if (_editors[i].uuid !== uuid) continue;

            leftEditor  = _editors[i - 1];
            rightEditor = _editors[i];

        }

        leftEditor.rightSiblingUUID = rightEditor.uuid;
        rightEditor.leftSiblingUUID = leftEditor.uuid;
    }

    public setSession(file: NewtonFile | undefined | null) {
        if ( !file ) return;

        let editorComponent = this.getActiveEditorComponent();
        editorComponent.assignSession(file);
        this.miniMapView.cloneSession(file);
    }

    public newFile() {
        let editorComponent = this.getActiveEditorComponent();

        editorComponent.newFile();
        this.miniMapView.newFile();
    }

    public getSession() {
        let editorComponent = this.get(this.activeEditor);
        let editor          = editorComponent.editor;

        return editor.getSession();
    }

    public async setActiveEditor(activeEditor: string) {
        this.activeEditor       = activeEditor;
        let editorComponent     = this.getActiveEditorComponent();

        if (!this.miniMapView) return;

        if (editorComponent.activeFile) {
            this.miniMapView.cloneSession(editorComponent.activeFile);
            return;
        }

        // Note: likely a new file/buffer
        this.miniMapView.editor.session.setValue(
            editorComponent.editor.session.getValue()
        );
    }

    public getActiveEditorComponent(): any {
        return this.get(this.activeEditor);
    }

    protected getActiveEditor(): any {
        let editorComponent = this.get(this.activeEditor);
        let editor          = editorComponent.editor;
        return editor;
    }


    public sendMessage(data: ServiceMessage): void {
        this.messageSubject.next(data);
    }

    public getMessage$(): Observable<ServiceMessage> {
        return this.messageSubject.asObservable();
    }

}