import {
    Directive,
    Output,
    EventEmitter,
    HostListener
} from '@angular/core';



@Directive({
    selector: '[draggable-item]'
})
export class DraggableDirective {
    @Output() dragStart = new EventEmitter<PointerEvent>();
    @Output() dragMove  = new EventEmitter<PointerEvent>();
    @Output() dragEnd   = new EventEmitter<PointerEvent>();

    private dragging    = false;
    selected: any;
    

    @HostListener('pointerdown', ['$event'])
    onPointerDown(event: PointerEvent): void {
        console.log("pointerdown");

        this.dragStart.emit(event);
    }

    @HostListener('document:pointermove', ['$event'])
    onPointerMove(event: PointerEvent): void {
        if (!this.dragging) return;
        console.log("pointermove");

        this.dragging = true;
        this.dragMove.emit(event);
    }

    @HostListener('document:pointerup', ['$event'])
    onPointerUp(event: PointerEvent): void {
        if (!this.dragging) return;

        console.log("pointerup");

        this.dragging = false;
        this.dragEnd.emit(event);
    }

}