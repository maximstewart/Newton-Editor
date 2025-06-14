import { ComponentRef, Injectable } from '@angular/core';
import { BehaviorSubject, ReplaySubject, Observable } from 'rxjs';

import { NewtonEditorComponent } from "../../../editor/newton-editor/newton-editor.component";

import { ServiceMessage } from '../../types/service-message.type';
import { EditorSettings } from "../../configs/editor.config";



@Injectable({
    providedIn: 'root'
})
export class EditorsService {
    private messageSubject: ReplaySubject<ServiceMessage> = new ReplaySubject<ServiceMessage>(1);
    private activationSubject: ReplaySubject<string>      = new ReplaySubject<string>(1);
    private switchSessionSubject: ReplaySubject<string>   = new ReplaySubject<string>(1);
    private closeTabSubject: ReplaySubject<string>        = new ReplaySubject<string>(1);
    private selectSessionLeftSubject: ReplaySubject<any>  = new ReplaySubject<any>(1);
    private selectSessionRightSubject: ReplaySubject<any> = new ReplaySubject<any>(1);
    private moveSessionLeftSubject: ReplaySubject<any>    = new ReplaySubject<any>(1);
    private moveSessionRightSubject: ReplaySubject<any>   = new ReplaySubject<any>(1);

    editors: Map<string, ComponentRef<NewtonEditorComponent>>;
    editorSettings: typeof EditorSettings;


    constructor() {
        this.editorSettings = EditorSettings;
        this.editors = new Map<string, ComponentRef<NewtonEditorComponent>>();
    }


    getEditorsAsArray(): ComponentRef<NewtonEditorComponent>[] {
        return [...this.editors.values()];
    }

    get(uuid: string): NewtonEditorComponent {
        return this.editors.get(uuid).instance;
    }

    set(uuid: string, component: ComponentRef<NewtonEditorComponent>) {
        this.editors.set(uuid, component);
    }


    setData(data: ServiceMessage): void {
        this.messageSubject.next(data);
    }

    getData$(): Observable<ServiceMessage> {
        return this.messageSubject.asObservable();
    }

    setActiveEditor(data: string): void {
        this.activationSubject.next(data);
    }

    newActiveEditor$(): Observable<string> {
        return this.activationSubject.asObservable();
    }

    setTabToEditor(data: string): void {
        this.switchSessionSubject.next(data);
    }

    loadTabToEditor$(): Observable<string> {
        return this.switchSessionSubject.asObservable();
    }

    closeTab(data: string): void {
        this.closeTabSubject.next(data);
    }

    closeTabRequested$(): Observable<string> {
        return this.closeTabSubject.asObservable();
    }

    moveSessionLeft(data: string): void {
        this.moveSessionLeftSubject.next(data);
    }

    moveSessionLeftRequested$(): Observable<string> {
        return this.moveSessionLeftSubject.asObservable();
    }

    moveSessionRight(data: string): void {
        this.moveSessionRightSubject.next(data);
    }

    moveSessionRightRequested$(): Observable<string> {
        return this.moveSessionRightSubject.asObservable();
    }

    selectSessionLeft(data: string): void {
        this.selectSessionLeftSubject.next(data);
    }

    selectSessionLeftRequested$(): Observable<string> {
        return this.selectSessionLeftSubject.asObservable();
    }

    selectSessionRight(data: string): void {
        this.selectSessionRightSubject.next(data);
    }

    selectSessionRightRequested$(): Observable<string> {
        return this.selectSessionRightSubject.asObservable();
    }

}