import { Component, inject } from '@angular/core';

import { EditorsService } from '../../common/services/editor/editors.service';



@Component({
    selector: 'editor-resize',
    standalone: true,
    imports: [
    ],
    templateUrl: './editor-resize.component.html',
    styleUrl: './editor-resize.component.css',
    host: {
        'class': 'row'
    }
})
export class EditorResizeComponent {

    private editorsService: EditorsService = inject(EditorsService);


    constructor() {
    }


    // Note: Only really works with 2 editors and very brittle logic.
    protected setEditorSize(event: any) {
        let lEditorComponent = null;
        let rEditorComponent = null;
        let lSize = 6;
        let rSize = 6;

        if (
            event.target.parentElement.classList.contains("editor-left-size")
        ) {
            lSize   = parseInt(
                event.target.classList[1].split("-")[1]
            );
            rSize   = 12 - lSize;

            lEditorComponent = this.editorsService.getActiveEditorComponent();
            if (lEditorComponent.leftSiblingUUID) {
                rEditorComponent = lEditorComponent;
                lEditorComponent = this.editorsService.get(lEditorComponent.leftSiblingUUID);
            } else {
                rEditorComponent = this.editorsService.get(lEditorComponent.rightSiblingUUID);
            }
        } else {
            rSize   = parseInt(
                event.target.classList[1].split("-")[1]
            );
            lSize   = 12 - rSize;
            rEditorComponent = this.editorsService.getActiveEditorComponent();
            if (rEditorComponent.rightSiblingUUID) {
                lEditorComponent = rEditorComponent;
                rEditorComponent = this.editorsService.get(rEditorComponent.rightSiblingUUID);
            } else {
                lEditorComponent = this.editorsService.get(rEditorComponent.leftSiblingUUID);
            }
        }

        this.resizeAndFocus(lEditorComponent, lSize, rEditorComponent, rSize);
    }

    private resizeAndFocus(lEditorComponent: any, lSize: number, rEditorComponent: any, rSize: number) {
        let lElm = lEditorComponent.editorElm.nativeElement.parentElement;
        let rElm = rEditorComponent.editorElm.nativeElement.parentElement;

        lElm.setAttribute(
            'class',
            (lSize == 0) ? "hidden" : `col col-${lSize}`
        );

        rElm.setAttribute(
            'class',
            (rSize == 0) ? "hidden" : `col col-${rSize}`
        );

        if (lSize == 0) rEditorComponent.editor.focus();
        if (rSize == 0) lEditorComponent.editor.focus();
    }

}