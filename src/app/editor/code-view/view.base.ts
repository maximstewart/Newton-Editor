import { Directive, ElementRef, Input, ViewChild, inject } from '@angular/core';
import * as uuid from 'uuid';

import { InfoBarService } from '../../common/services/editor/info-bar/info-bar.service';
import { FilesModalService } from '../../common/services/editor/modals/files-modal.service';
import { TabsService } from '../../common/services/editor/tabs/tabs.service';
import { EditorsService } from '../../common/services/editor/editors.service';
import { FilesService } from '../../common/services/editor/files.service';

import { EditorSettings } from "../../common/configs/editor.config";
import { NewtonFile } from '../../common/types/file.type';

import { ServiceMessage } from '../../common/types/service-message.type';



@Directive()
export class CodeViewBase {
    public uuid: string                            = uuid.v4();
    @Input() public isDefault: boolean             = false;
    @Input() public isMiniMap: boolean             = false;
    public leftSiblingUUID!: string;
    public rightSiblingUUID!: string;

    protected infoBarService: InfoBarService       = inject(InfoBarService);
    protected filesModalService: FilesModalService = inject(FilesModalService);
    protected tabsService: TabsService             = inject(TabsService);
    protected editorsService: EditorsService       = inject(EditorsService);
    protected filesService: FilesService           = inject(FilesService);

    @ViewChild('editor') editorElm!: ElementRef;
    @Input() editorSettings!: typeof EditorSettings;

    public editor!: any;
    public activeFile!: NewtonFile;

    public cutBuffer: string = "";
    public timerId: number   = -1;


    constructor() {
    }


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

    public search() {
        console.log(this.editor.session.getMode()["$id"]);
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
                let fpath = data.value;
                let path  = "";

                for (let i = 0; i < stubPaths.length; i++) {
                    if (stubPaths[i] === fpath) {
                        path = paths[i];
                    }
                }

                if (!path) return;

                this.activeFile = this.filesService.get(path);
                this.editor.setSession(this.activeFile.session);
            }
        });

    }

    public destroySession() {
        this.editor.session.destroy();
    }

    public toggleFullScreen() {
        window.main.toggleFullScreen();
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
        this.editorElm.nativeElement.parentElement.classList.add("col-1");
        this.editorElm.nativeElement.parentElement.classList.add("zero-margin-padding");
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

    private quit() {
        window.main.quit();
    }
}