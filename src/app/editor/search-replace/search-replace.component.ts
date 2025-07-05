import { Component, ElementRef, HostBinding, Input, ViewChild, inject } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

import { SearchReplaceService } from '../../common/services/editor/search-replace/search-replace.service';

import { ServiceMessage } from '../../common/types/service-message.type';



@Component({
    selector: 'search-replace',
    standalone: true,
    imports: [
    ],
    templateUrl: './search-replace.component.html',
    styleUrl: './search-replace.component.css',
    host: {
        'class': 'row search-replace',
        "(keyup)": "globalSearchReplaceKeyHandler($event)"
    }
})
export class SearchReplaceComponent {
    private unsubscribe: Subject<void>                 = new Subject();

    private searchReplaceService: SearchReplaceService = inject(SearchReplaceService);

    @HostBinding("class.hidden") isHidden: boolean     = true;
    @ViewChild('findEntryElm') findEntryElm!: ElementRef;
    @ViewChild('replaceEntryElm') replaceEntryElm!: ElementRef;

    private editor!: any;

    @Input() findOptions: string           = "";
    private useWholeWordSearch: boolean    = false;
    private searchOnlyInSelection: boolean = false;
    private useCaseSensitive: boolean      = false;
    private useRegex: boolean              = false;
    private selection: string              = "";
    private query: string                  = "";
    private toStr: string                  = "";
    private isBackwards: boolean           = false;
    private isWrap: boolean                = true;
    private searchTimeoutId: number        = -1;
    private searchTimeout: number          = 400;


    constructor() {
    }


    private ngAfterViewInit(): void {
        this.loadSubscribers();
    }

    private ngOnDestroy() {
        this.unsubscribe.next();
        this.unsubscribe.complete();
    }

    private loadSubscribers() {
        this.searchReplaceService.getMessage$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((message: ServiceMessage) => {
            if (message.action === "toggle-search-replace") {
                this.toggleSearchReplace(message);
            } else if (message.action === "set-active-editor") {
                this.setActiveEditor(message);
            }
        });
    }

    private toggleSearchReplace(message: ServiceMessage) {
        this.selection = this.editor.getSelectedText();
        this.findEntryElm.nativeElement.value = this.selection;

        if (this.selection && !this.isHidden) {
            this.findEntryElm.nativeElement.focus();
            return;
        }

        this.isHidden = !this.isHidden;

        if (this.isHidden) {
            this.editor.focus();
            return;
        }

        setTimeout(() => {
            this.findEntryElm.nativeElement.focus();
        }, 200);
    }

    private setActiveEditor(message: ServiceMessage) {
        if (this.editor == message.rawData) return;

        this.editor = message.rawData;

        if (this.isHidden) return;


        this.searchForString();
    }

    public hideSearchReplace() {
        if (this.selection) {
            this.selection = "";
            return;
        }

        this.isHidden = true;
        this.editor.focus();
    }

    public globalSearchReplaceKeyHandler(event: any) {
        if (event.ctrlKey && event.key === "f") {
            this.hideSearchReplace();
        } else if (event.ctrlKey && event.key === "l") {
            this.findEntryElm.nativeElement.focus();
        } else if (event.ctrlKey && event.key === "r") {
            this.replaceEntryElm.nativeElement.focus();
        }
    }

    public toggleWholeWordSearch(event: any) {
        let target = event.target;
        if (target.nodeName === "IMG")
            target = target.parentElement;

        this.useWholeWordSearch = !this.useWholeWordSearch;
        target.classList.toggle("selected");
        this.setFindOptionsLbl();
        this.findAllEntries();
    }

    public toggleSelectionOnlyScan(event: any) {
        let target = event.target;
        if (target.nodeName === "IMG")
            target = target.parentElement;

        this.searchOnlyInSelection = !this.searchOnlyInSelection;
        target.classList.toggle("selected");
        this.setFindOptionsLbl();
        this.findAllEntries();
    }

    public toggleCaseSensitive(event: any) {
        this.useCaseSensitive = !this.useCaseSensitive;
        event.target.classList.toggle("selected");
        this.setFindOptionsLbl();
        this.findAllEntries();
    }

    public toggleRegex(event: any) {
        this.useRegex = !this.useRegex;
        event.target.classList.toggle("selected");
        this.setFindOptionsLbl();
        this.findAllEntries();
    }

    private setFindOptionsLbl() {
        let findOptionsStr = "";

        if (this.useRegex)
            findOptionsStr += "Regex"

        findOptionsStr += (findOptionsStr) ? ", " : "";
        findOptionsStr += (this.useCaseSensitive) ? "Case Sensitive" : "Case InSensitive";

        if (this.searchOnlyInSelection)
            findOptionsStr += ", Within Current Selection"

        if (this.useWholeWordSearch)
            findOptionsStr += ", Whole Word"

        this.findOptions = findOptionsStr;
    }


    public findNextEntry() {
        this.editor.findNext();
    }

    public findAllEntries() {
        this.query = this.findEntryElm.nativeElement.value;

        if (!this.query) return;

        let totalCount = this.editor.findAll(this.query, {
            backwards: this.isBackwards,
            wrap: this.isWrap,
            caseSensitive: this.useCaseSensitive,
            wholeWord: this.useWholeWordSearch,
            regExp: this.useRegex,
            range: this.searchOnlyInSelection
        });
    }

    public findPreviousEntry() {
        this.editor.findPrevious();
    }

    public replaceEntry(event: any) {
        if (event instanceof KeyboardEvent) {
            if (event.key !== "Enter") {
                return;
            }
        }

        let fromStr = this.findEntryElm.nativeElement.value;
        let toStr   = this.replaceEntryElm.nativeElement.value;

        if (!fromStr) return;

        let totalCount = this.editor.replace(toStr, fromStr, {
            backwards: this.isBackwards,
            wrap: this.isWrap,
            caseSensitive: this.useCaseSensitive,
            wholeWord: this.useWholeWordSearch,
            regExp: this.useRegex,
            range: this.searchOnlyInSelection
        });

        this.editor.clearSelection();
        this.editor.findNext();
    }

    public replaceAll() {
        let fromStr = this.findEntryElm.nativeElement.value;
        let toStr   = this.replaceEntryElm.nativeElement.value;

        if (!fromStr) return;

        let totalCount = this.editor.replaceAll(toStr, fromStr, {
            backwards: this.isBackwards,
            wrap: this.isWrap,
            caseSensitive: this.useCaseSensitive,
            wholeWord: this.useWholeWordSearch,
            regExp: this.useRegex,
            range: this.searchOnlyInSelection
        });
    }

    public searchForString() {
        if (event instanceof KeyboardEvent) {
            if (event.key !== "Enter") {
                return;
            }
        }

        this.query = this.findEntryElm.nativeElement.value;

        if (!this.query) return;

        if (this.searchTimeoutId) { clearTimeout(this.searchTimeoutId); }

        this.searchTimeoutId = setTimeout(() => {
            let totalCount = this.editor.find(this.query, {
                backwards: this.isBackwards,
                wrap: this.isWrap,
                caseSensitive: this.useCaseSensitive,
                wholeWord: this.useWholeWordSearch,
                regExp: this.useRegex,
                range: this.searchOnlyInSelection
            });
        }, this.searchTimeout);
    }

}