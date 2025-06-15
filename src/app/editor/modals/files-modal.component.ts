import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";

import { Subject, takeUntil } from 'rxjs';

import * as bootstrap from "bootstrap";

import { FilesModalService } from "../../common/services/editor/modals/files-modal.service";
import { TabsService } from '../../common/services/editor/tabs/tabs.service';

import { ServiceMessage } from '../../common/types/service-message.type';



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
    private unsubscribe = new Subject<void>();

    filesModal!: bootstrap.Modal;
    files: any[] = [];


    constructor(
        private filesModalService: FilesModalService,
        private tabsService: TabsService
    ) {
    }


    public ngAfterViewInit(): void {
        this.loadSubscribers();
    }

    loadSubscribers() {
        this.tabsService.getData$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((data: ServiceMessage) => {
            if (data.action === "create-tab") {
                this.createFileRow(data.message, data.uuid, data.data);
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

    private createFileRow(title: string, uuid: string, path: string): void {
        this.files.push({title: title, path: path, uuid: uuid})
    }

    createModal() {
        this.filesModal = new bootstrap.Modal("#filesModal", {});
    }

    showModal() {
        this.filesModal?.toggle();
    }

}