import { Directive, ElementRef, Input, ViewChild } from '@angular/core';

import { EditorSettings } from "../../common/configs/editor.config";



@Directive()
export class AceEditorBase {
    @ViewChild('editor') editorElm!: ElementRef;
    @Input() editorSettings!: typeof EditorSettings;
    editor!: any;
    uuid!: string;
    fontSize: number  = 12;
    cutBuffer: string = "";
    timerId: number   = -1;


    constructor(
    ) {}


    protected zoomIn() {
        this.fontSize += 1;
        this.editorElm.nativeElement.style.fontSize = `${this.fontSize}px`;
    }

    protected zoomOut() {
        this.fontSize -= 1;
        this.editorElm.nativeElement.style.fontSize = `${this.fontSize}px`;
    }

    protected search() {
        console.log(this.editor.getSession()["$modeId"])
    }

    protected movelinesUp() {
        this.editor.execCommand("movelinesup");
    }

    protected movelinesDown() {
        this.editor.execCommand("movelinesdown");
    }

    protected duplicateLines() {
        this.editor.execCommand("copylinesdown");
    }

    protected cutToBuffer() {
        if (this.timerId) { clearTimeout(this.timerId); }

        const cursorPosition = this.editor.getCursorPosition();
        let lineText         = this.editor.session.getLine(cursorPosition.row);
        this.cutBuffer       += `${lineText}\n`;
        this.editor.session.removeFullLines(cursorPosition.row, cursorPosition.row)

        this.setBufferClearTimeout();
    }

    protected pasteCutBuffer() {
        if (this.timerId) { clearTimeout(this.timerId); }

        const cursorPosition = this.editor.getCursorPosition();
        this.editor.session.insert(cursorPosition, this.cutBuffer)

        this.setBufferClearTimeout();
    }

    private setBufferClearTimeout(timeout: number = 5000) {
        this.timerId = setTimeout(() => {
            this.cutBuffer = "";
            this.timerId   = -1;
        }, timeout);
    }

}