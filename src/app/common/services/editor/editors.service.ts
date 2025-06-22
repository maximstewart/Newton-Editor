import { ComponentRef, Injectable } from '@angular/core';
import { ReplaySubject, Observable } from 'rxjs';

import { NewtonEditorComponent } from "../../../editor/newton-editor/newton-editor.component";

import { ServiceMessage } from '../../types/service-message.type';
import { EditorSettings } from "../../configs/editor.config";



@Injectable({
    providedIn: 'root'
})
export class EditorsService {
    private messageSubject: ReplaySubject<ServiceMessage> = new ReplaySubject<ServiceMessage>(1);

    editors: Map<string, ComponentRef<NewtonEditorComponent>>;
    editorSettings: typeof EditorSettings;


    constructor() {
        this.editorSettings = EditorSettings;
        this.editors = new Map<string, ComponentRef<NewtonEditorComponent>>();
    }


    public getEditorsAsArray(): ComponentRef<NewtonEditorComponent>[] {
        return [...this.editors.values()];
    }

    public get(uuid: string): NewtonEditorComponent {
        return this.editors.get(uuid).instance;
    }

    public set(uuid: string, component: ComponentRef<NewtonEditorComponent>) {
        this.editors.set(uuid, component);
    }


    public sendMessage(data: ServiceMessage): void {
        this.messageSubject.next(data);
    }

    public getMessage$(): Observable<ServiceMessage> {
        return this.messageSubject.asObservable();
    }

}