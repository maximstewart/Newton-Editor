import {
    Component,
    DestroyRef,
    HostBinding,
    inject
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { marked } from 'marked';

import { MarkdownPreviewService } from '../../common/services/editor/markdown-preview/markdown-preview.service';

import { ServiceMessage } from '../../common/types/service-message.type';



@Component({
    selector: 'markdown-preview',
    standalone: true,
    imports: [
    ],
    templateUrl: './markdown-preview.component.html',
    styleUrl: './markdown-preview.component.css',
    host: {
        'class': 'container-fluid markdown-preview'
    }
})
export class MarkdownPreviewComponent {
    readonly #destroyRef: DestroyRef                       = inject(DestroyRef);

    private markdownPreviewService: MarkdownPreviewService = inject(MarkdownPreviewService);

    @HostBinding("class.hidden") isHidden: boolean         = true;
    converter: any                                         = marked;
    defaultHtml: string                                    = "<h1>NOT a Markdown file...</h1>"
    bodyHtml: string                                       = "";

    private editorComponent!: any;


    constructor() {
        this.loadSubscribers();
    }

    private loadSubscribers() {
        this.markdownPreviewService.getMessage$().pipe(
            takeUntilDestroyed(this.#destroyRef)
        ).subscribe((message: ServiceMessage) => {
            switch ( message.action ) {
                case "toggle-markdown-preview":
                    this.toggleMarkdownPreview(message);
                    break;
                case "set-active-editor":
                    this.setActiveEditor(message);
                    break;
                default:
                    break;
            }
        });
    }

    private toggleMarkdownPreview(message: ServiceMessage) {
        this.isHidden = !this.isHidden;

        setTimeout(() => {
            this.updatePreview();
        }, 10);
    }

    private setActiveEditor(message: ServiceMessage) {
        if (this.editorComponent == message.rawData) return;

        this.editorComponent = message.rawData;

        if (this.isHidden) return;

        this.updatePreview();
    }

    public updatePreview() {
        let fileMode  = this.editorComponent.editor.session.getMode()["$id"];
        let isMdFile  = (fileMode.includes("markdown"));
        this.bodyHtml = "";

        if (!isMdFile) return;

        let mdStr     = this.editorComponent.editor.session.getValue();
        let pathParts = this.editorComponent.activeFile.path.split("/");
        let basePath  = "file://" + pathParts.slice(0, -1).join("/");
        this.bodyHtml = this.converter.parse(
            mdStr.replaceAll("](images", `](${basePath}/images`)
                .replaceAll("](imgs", `](${basePath}/imgs`)
                .replaceAll("](pictures", `](${basePath}/pictures`)
                .replaceAll("](pics", `](${basePath}/pics`)
                .replaceAll("](screenshots", `](${basePath}/screenshots`)
        );
    }

}