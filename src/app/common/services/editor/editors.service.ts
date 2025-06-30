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
        this.editors.set(uuid, component);

        if (Object.keys(this.editors).length < 1) return;

        let leftEditor  = null;
        let rightEditor = null;
        let _editors    = this.getEditorsAsArray();

        for (let i = 0; i < _editors.length; i++) {
            if (_editors[i].uuid !== uuid) continue;

            leftEditor  = _editors[i - 1];
            rightEditor = _editors[i];

        }

        leftEditor.rightSiblingUUID = rightEditor.uuid;
        rightEditor.leftSiblingUUID = leftEditor.uuid;
    }

    public async setSession(file: NewtonFile | undefined | null) {
        if ( !file ) return;

        let editorComponent        = this.getActiveEditorComponent();
        let editor                 = editorComponent.editor;

        editorComponent.activeFile = file;
        editor.setSession(file.session);
    }

    public getSession() {
        let editorComponent = this.get(this.activeEditor);
        let editor          = editorComponent.editor;

        return editor.getSession();
    }

    public setActiveEditor(activeEditor: string) {
        this.activeEditor = activeEditor;
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