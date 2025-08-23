import {
    Directive,
    ElementRef,
    Input,
    ViewChild,
    inject
} from '@angular/core';
import * as uuid from 'uuid';

import { InfoBarService } from '../../common/services/editor/info-bar/info-bar.service';
import { FilesModalService } from '../../common/services/editor/modals/files-modal.service';
import { TabsService } from '../../common/services/editor/tabs/tabs.service';
import { EditorsService } from '../../common/services/editor/editors.service';
import { FilesService } from '../../common/services/files.service';
import { SearchReplaceService } from '../../common/services/editor/search-replace/search-replace.service';
import { MarkdownPreviewService } from '../../common/services/editor/markdown-preview/markdown-preview.service';
import { LspManagerService } from '../../common/services/editor/lsp-manager/lsp-manager.service';

import { EditorSettings } from "../../common/configs/editor.config";
import { NewtonFile } from '../../common/types/file.type';

import { ServiceMessage } from '../../common/types/service-message.type';



@Directive()
export class CodeViewBase {
    public uuid: string                   = uuid.v4();
    @Input() public isDefault: boolean    = false;
    @Input() public mode: string          = "";
    public leftSiblingUUID!: string;
    public rightSiblingUUID!: string;

    protected infoBarService: InfoBarService                 = inject(InfoBarService);
    protected filesModalService: FilesModalService           = inject(FilesModalService);
    protected tabsService: TabsService                       = inject(TabsService);
    protected editorsService: EditorsService                 = inject(EditorsService);
    protected filesService: FilesService                     = inject(FilesService);
    protected searchReplaceService: SearchReplaceService     = inject(SearchReplaceService);
    protected markdownPreviewService: MarkdownPreviewService = inject(MarkdownPreviewService);
    protected lspManagerService: LspManagerService           = inject(LspManagerService);

    @ViewChild('editor') editorElm!: ElementRef;
    @Input() editorSettings!: typeof EditorSettings;

    public editor!: any;
    public aceApi!: any;
    public activeFile!: NewtonFile;

    public cutBuffer: string    = "";
    public timerId: number      = -1;
    public debounceId: number   = -1;
    public debounceWait: number = 800;

    @ViewChild('contextMenu') contextMenu!: ElementRef;
    public showContextMenu: boolean = false;


    public selectLeftEditor() {
        let message        = new ServiceMessage();
        message.action     = "select-left-editor";
        message.editorUUID = this.uuid;

        this.editorsService.sendMessage(message);
    }

    public selectRightEditor() {
        let message        = new ServiceMessage();
        message.action     = "select-right-editor";
        message.editorUUID = this.uuid;

        this.editorsService.sendMessage(message);
    }

    public moveSessionLeft() {
        let message        = new ServiceMessage();
        message.action     = "move-session-left";
        message.editorUUID = this.uuid;

        this.editorsService.sendMessage(message);
    }

    public moveSessionRight() {
        let message        = new ServiceMessage();
        message.action     = "move-session-right";
        message.editorUUID = this.uuid;

        this.editorsService.sendMessage(message);
    }

    public addActiveStyling() {
        this.editorElm.nativeElement.classList.add("active-editor")
    }

    public removeActiveStyling() {
        this.editorElm.nativeElement.classList.remove("active-editor")
    }

    public openCommandPalette2() {
        this.editor.execCommand("openCommandPalette");
    }

    public showKeyShortcuts() {
        this.editor.showKeyboardShortcuts();
    }

    public lspManagerPopup() {
        let message        = new ServiceMessage();
        message.action     = "toggle-lsp-manager";
        this.lspManagerService.sendMessage(message);
    }

    public markdownPreviewPopup() {
        let message        = new ServiceMessage();
        message.action     = "toggle-markdown-preview";
        this.markdownPreviewService.sendMessage(message);
    }

    public searchPopup() {
        let message        = new ServiceMessage();
        message.action     = "toggle-search-replace";
        this.searchReplaceService.sendMessage(message);

        // this.editor.execCommand("find");
    }

    public replacePopup() {
        let message        = new ServiceMessage();
        message.action     = "toggle-search-replace";
        this.searchReplaceService.sendMessage(message);

        // this.editor.execCommand("replace");
    }

    public showFilesList() {
        let paths     = this.filesService.getAllPaths();
        let stubPaths = [];

        for (let i = 0; i < paths.length; i++) {
            let fpath = paths[i];
            if (fpath.length > 67) {
                fpath = "..." + fpath.slice(fpath.length - 67, fpath.length);
            }
            stubPaths.push(fpath);
        }

        this.editor.prompt("",
        {
            name: "Files:",
            placeholder: "Search...",
            getCompletions: (search) => {
                let query  = search.getValue();
                let result = [];

                if (!query) return stubPaths;

                for (let i = 0; i < stubPaths.length; i++) {
                    if (stubPaths[i].includes(query)) {
                        result.push(stubPaths[i]);
                    }
                }

                return result;
            },
            onAccept: (data) => {
                let fpath = (data.value) ? data.value : data.item;
                let path  = "";

                for (let i = 0; i < stubPaths.length; i++) {
                    if (stubPaths[i] === fpath) {
                        path = paths[i];
                    }
                }

                if (!path) return;

                this.editorsService.setSession(
                    this.filesService.get(path)
                );
            }
        });

    }

    public closeFile() {
        this.tabsService.closeTab(this.activeFile.path);
    }

    public toggleFullScreen() {
        window.main.toggleFullScreen();
    }

    public setAsReadOnly() {
        this.editor.setReadOnly(true);
        this.editor.setShowPrintMargin(false);
    }

    public setAsMiniMapView() {
        this.editor.renderer.showLineNumbers = false;
        this.editor.renderer.setShowGutter(false);

        this.editor.setReadOnly(true);
        this.editor.setFontSize(2);
        this.editor.setHighlightActiveLine(false);
        this.editor.setHighlightGutterLine(false);
        this.editor.setShowFoldWidgets(false);
        this.editor.setShowPrintMargin(false);
        this.editor.session.setUseWrapMode(true);

        this.editorElm.nativeElement.parentElement.classList.add("col-1");
        this.editorElm.nativeElement.parentElement.classList.add("zero-margin-padding");

        this.editor.on("click", (event) => {
            event.preventDefault();
            event.stopPropagation();

            let editorComponent = this.editorsService.getActiveEditorComponent();
            let pos             = this.editor.getCursorPosition();

            editorComponent.editor.moveCursorToPosition(pos);
            editorComponent.editor.clearSelection();
            editorComponent.editor.renderer.scrollCursorIntoView(null, 0.5);
        });

        this.editor.on("mousewheel", (event) => {
            event.preventDefault();
            event.stopPropagation();

            let editorComponent = this.editorsService.getActiveEditorComponent();
            editorComponent.editor.renderer.scrollBy(null, event.domEvent.deltaY);
        });
    }

    public zoomIn() {
        this.editor.setFontSize(
            parseInt(this.editor.getFontSize()) + 1
        );
    }

    public zoomOut() {
        this.editor.setFontSize(
            parseInt(this.editor.getFontSize()) - 1
        );
    }

    public movelinesUp() {
        this.editor.execCommand("movelinesup");
    }

    public movelinesDown() {
        this.editor.execCommand("movelinesdown");
    }

    public duplicateLines() {
        this.editor.execCommand("copylinesdown");
    }

    public cutText() {
        let cutText = this.editor.getSelectedText();
        this.editor.remove();
        navigator.clipboard.writeText(cutText).catch(() => {
            console.error("Unable to cut text...");
        });
    }

    public copyText() {
        let copyText = this.editor.getSelectedText();
        navigator.clipboard.writeText(copyText).catch(() => {
            console.error("Unable to copy text...");
        });
    }

    public pasteText() {
        navigator.clipboard.readText().then((pasteText) => {
            this.editor.insert(pasteText, true);
        });
    }

    protected updateInfoBar() {
        this.infoBarService.setInfoBarFPath(this.activeFile?.path)
        this.infoBarService.setInfoBarCursorPos(
            this.editor.getCursorPosition()
        );
        this.infoBarService.setInfoBarFType(
            this.editor.session.getMode()["$id"]
        );
    }

    public newFile() {
        this.activeFile = null;
        let session     = this.aceApi.createEditSession([""]);
        this.editor.setSession(session);
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
        window.fs.saveFileAs().then((path: string) => {
            if (!path) return;

            let file: NewtonFile = new File([""], path, {});
            const text           = this.editor.session.getValue();

            window.fs.saveFile(path, text);
            this.filesService.addFile(
                path,
                file,
                false,
                text
            ).then(() => {
                this.activeFile = this.filesService.get(path);
                this.editor.setSession(this.activeFile.session);
                this.filesService.addTab(this.activeFile);
            });

        });
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

    private quit() {
        window.main.quit();
    }
}