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
    @Output() dragStart: EventEmitter<PointerEvent> = new EventEmitter();
    @Output() dragMove: EventEmitter<PointerEvent>  = new EventEmitter();
    @Output() dragEnd: EventEmitter<PointerEvent>   = new EventEmitter();

    private dragging: boolean = false;
    selected: any;
    

    @HostListener('pointerdown', ['$event'])
    onPointerDown(event: PointerEvent): void {
        console.log("pointerdown");
        this.dragging = true;

        this.dragStart.emit(event);
    }

    @HostListener('document:pointermove', ['$event'])
    onPointerMove(event: PointerEvent): void {
        if (!this.dragging) return;
        console.log("pointermove");

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