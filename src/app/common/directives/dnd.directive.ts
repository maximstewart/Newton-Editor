import {
    Directive,
    Output,
    Input,
    EventEmitter,
    HostBinding,
    HostListener
} from '@angular/core';

import { NewtonFile } from '../types/file.type';



@Directive({
    selector: '[dropzone]'
})
export class DndDirective {
    @HostBinding('class.fileover') fileOver!: boolean;
    @Output() fileDropped: EventEmitter<any> = new EventEmitter();

    @HostListener('dragover', ['$event'])
    onDragOver(evt: any) {
        evt.preventDefault();
        evt.stopPropagation();

        this.fileOver = true;
    }

    @HostListener('dragleave', ['$event'])
    public onDragLeave(evt: any) {
        evt.preventDefault();
        evt.stopPropagation();

        this.fileOver = false;
    }

    @HostListener('drop', ['$event'])
    publicondrop(evt: any) {
        evt.preventDefault();
        evt.stopPropagation();

        this.fileOver                = false;
        let files: Array<NewtonFile> = evt.dataTransfer.files;

        if (files.length == 0) return;

        this.fileDropped.emit(files);
    }

}