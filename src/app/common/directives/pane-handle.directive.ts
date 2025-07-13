import {
    Directive,
    Output,
    EventEmitter,
    HostListener
} from '@angular/core';



@Directive({
    selector: '[pane-handle]'
})
export class PaneHandleDirective {
    @Output() dragStart = new EventEmitter<PointerEvent>();
    @Output() dragMove  = new EventEmitter<PointerEvent>();
    @Output() dragEnd   = new EventEmitter<PointerEvent>();

    private dragging: boolean = false;
    private isHrPane: boolean = false;
    private parentElm: any;
    private leftSiblingElm: any;
    private rightSiblingElm: any;


    @HostListener('pointerdown', ['$event'])
    onPointerDown(event: PointerEvent): void {
        event.preventDefault();

        let target = event.target as Element;
        if (
            !target.classList.contains("hr-pane-handle") &&
            !target.classList.contains("vr-pane-handle")
        ) {
            console.error("Must have 'hr-pane-handle' or 'vr-pane-handle' in classList!");
            return;
        }

        target.requestPointerLock();

        this.dragging        = true;
        this.isHrPane        = ( target.classList.contains("hr-pane-handle") ) ? true : false ;
        this.parentElm       = target.parentElement as Element;
        this.leftSiblingElm  = target.previousElementSibling as Element;
        this.rightSiblingElm = target.nextElementSibling as Element;

        this.dragStart.emit(event);
    }

    @HostListener('pointermove', ['$event'])
    onPointerMove(event: PointerEvent): void {
        if (!this.dragging) return;

        let x            = event.movementX;
        let y            = event.movementY;
        let parentBounds = this.parentElm.getBoundingClientRect();
        let leftBounds   = this.leftSiblingElm.getBoundingClientRect();
        let rightBounds  = this.rightSiblingElm.getBoundingClientRect();

        if (this.isHrPane) {
            this.leftSiblingElm.style.maxHeight  = `${leftBounds.height + y}px`;
            this.rightSiblingElm.style.maxHeight = `${rightBounds.height - y}px`;
        } else {
            this.leftSiblingElm.style.maxWidth  = `${leftBounds.width + x}px`;
            this.rightSiblingElm.style.maxWidth = `${rightBounds.width - x}px`;
        }

        this.dragMove.emit(event);
    }

    @HostListener('pointerup', ['$event'])
    onPointerUp(event: PointerEvent): void {
        if (!this.dragging) return;

        this.dragging     = false;
        this.leftSiblingElm  = null;
        this.rightSiblingElm = null;

        document.exitPointerLock();
        this.dragEnd.emit(event);
    }

}