import { Component, inject } from "@angular/core";
import { CommonModule } from "@angular/common";

import { Subject, takeUntil } from 'rxjs';

import * as bootstrap from "bootstrap";

import { FilesModalService } from "../../services/editor/modals/files-modal.service";
import { TabsService } from '../../services/editor/tabs/tabs.service';

import { ServiceMessage } from '../../types/service-message.type';



@Component({
    selector: 'files-modal',
    standalone: true,
    imports: [
        CommonModule
    ],
    templateUrl: './files-modal.component.html',
    styleUrl: './files-modal.component.css',
    host: {
        'class': ''
    }
})
export class FilesModalComponent {
    private unsubscribe: Subject<void>           = new Subject();

    private filesModalService: FilesModalService = inject(FilesModalService);
    private tabsService: TabsService             = inject(TabsService);

    filesModal!: bootstrap.Modal;
    files: any[] = [];


    constructor() {
    }


    private ngAfterViewInit(): void {
        this.loadSubscribers();
    }

    private loadSubscribers() {
        this.tabsService.getMessage$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((data: ServiceMessage) => {
            if (data.action === "create-tab") {
                this.createFileRow(data.fileName, data.fileUUID, data.filePath);
            }
        });

        this.filesModalService.showFilesModalRequested$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe(() => {
            if (!this.filesModal) {
                this.createModal();
            }

            this.showModal();
        });

        this.filesModalService.addFileToModalRequested$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((uuid: string) => {
            if (!this.filesModal) {
                this.createModal();
            }
        });
    }

    private createModal() {
        this.filesModal = new bootstrap.Modal("#filesModal", {});
    }

    public createFileRow(title: string, uuid: string, path: string): void {
        this.files.push({title: title, uuid: uuid, path: path})
    }

    public showModal() {
        this.filesModal?.toggle();
    }

}