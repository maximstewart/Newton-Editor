import { Directive, ElementRef, Input, ViewChild } from '@angular/core';

import { EditorSettings } from "../../common/configs/editor.config";



@Directive()
export class AceEditorBase {
    @ViewChild('editor') editorElm!: ElementRef;
    @Input() editorSettings!: typeof EditorSettings;
    editor!: any;
    uuid!: string;
    cutBuffer: string = "";
    timerId: number   = -1;


    constructor(
    ) {}


    protected search() {
        console.log(this.editor.getSession()["$modeId"])
    }

    protected saveFile() {
        const text = this.editor.session.getValue();
//        window.fs.saveFile(text);
    }

    protected saveFileAs() {
        const text = this.editor.session.getValue();
        window.fs.saveFileAs(text);
    }

    protected zoomIn() {
        this.editor.setFontSize(
            parseInt(this.editor.getFontSize()) + 1
        )
    }

    protected zoomOut() {
        this.editor.setFontSize(
            parseInt(this.editor.getFontSize()) - 1
        )
    }

    protected cutText() {
        let cutText = this.editor.getSelectedText();
        this.editor.remove();
        navigator.clipboard.writeText(cutText).catch(() => {
            console.error("Unable to cut text...");
        });
    }

    protected copyText() {
        let copyText = this.editor.getSelectedText();
        navigator.clipboard.writeText(copyText).catch(() => {
            console.error("Unable to copy text...");
        });
    }

    protected pasteText() {
        navigator.clipboard.readText().then((pasteText) => {
            this.editor.insert(pasteText, true);
        });
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

        this.editor.insert(this.cutBuffer, true);
        this.setBufferClearTimeout();
    }

    private setBufferClearTimeout(timeout: number = 5000) {
        this.timerId = setTimeout(() => {
            this.cutBuffer = "";
            this.timerId   = -1;
        }, timeout);
    }

}