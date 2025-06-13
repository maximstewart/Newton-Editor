import { Directive, ElementRef, Input, ViewChild } from '@angular/core';
import * as uuid from 'uuid';

import { EditorSettings } from "../../common/configs/editor.config";
import { NewtonFile } from '../../common/types/file.type';



@Directive()
export class NewtonEditorBase {
    @ViewChild('editor') editorElm!: ElementRef;
    @Input() editorSettings!: typeof EditorSettings;
    editor!: any;
    uuid!: string;
    cutBuffer: string = "";
    timerId: number   = -1;
    activeFile!: NewtonFile;
    isDefault: boolean = false;


    constructor(
    ) {
        this.uuid = uuid.v4();
    }


    public addActiveStyling() {
        this.editorElm.nativeElement.classList.add("active-editor")
    }

    public removeActiveStyling() {
        this.editorElm.nativeElement.classList.remove("active-editor")
    }

    public commander() {
        this.editor.execCommand("openCommandPalette");
    }

    protected search() {
        console.log(this.editor.session.getMode()["$id"]);
    }

    protected openFiles() {
        let startDir = "";
        if (this.activeFile) {
            let pathParts = this.activeFile.path.split("/");
            pathParts.pop();
            startDir = pathParts.join( '/' );
        }

        window.fs.openFiles(startDir);
    }

    protected saveFile() {
        if (!this.activeFile) {
            this.saveFileAs();
            return;
        }

        const text = this.activeFile.session.getValue();
        window.fs.saveFile(this.activeFile.path, text);
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