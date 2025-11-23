import {
    Component,
    DestroyRef,
    ElementRef,
    HostBinding,
    Input,
    ViewChild,
    inject
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

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
    readonly #destroyRef: DestroyRef                   = inject(DestroyRef);

    private searchReplaceService: SearchReplaceService = inject(SearchReplaceService);

    @HostBinding("class.hidden") isHidden: boolean     = true;
    @ViewChild('findEntryElm') findEntryElm!: ElementRef;
    @ViewChild('replaceEntryElm') replaceEntryElm!: ElementRef;

    @Input() query: string                 = "";
    @Input() findOptions: string           = "";
    @Input() isQueryLong: boolean          = false;
    @Input() isQueryNotFound: boolean      = false;
    @Input() totalCount: number            = 0;

    private editor!: any;

    private useWholeWordSearch: boolean    = false;
    private searchOnlyInSelection: boolean = false;
    private useCaseSensitive: boolean      = false;
    private useRegex: boolean              = false;
    private selection: string              = "";
    private toStr: string                  = "";
    private isBackwards: boolean           = false;
    private isWrap: boolean                = true;
    private searchTimeoutId: number        = -1;
    private searchTimeout: number          = 400;


    constructor() {
        this.loadSubscribers();
    }

    private loadSubscribers() {
        this.searchReplaceService.getMessage$().pipe(
            takeUntilDestroyed(this.#destroyRef)
        ).subscribe((message: ServiceMessage) => {
            switch ( message.action ) {
                case "toggle-search-replace":
                    this.toggleSearchReplace(message);
                    break;
                case "set-active-editor":
                    this.setActiveEditor(message);
                    break;
                default:
                    break;
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

    public findPreviousEntry() {
        this.editor.findPrevious();
    }

    public findNextEntry() {
        this.editor.findNext();
    }

    public findEntryKeyUpHandler(event: KeyboardEvent) {
        if (!event.ctrlKey || !this.query) return;

        if (event.key === "ArrowUp")   this.findPreviousEntry();
        if (event.key === "ArrowDown") this.findNextEntry();
    }

    public findAllEntries() {
        this.query = this.findEntryElm.nativeElement.value;

        this.totalCount = this.editor.findAll(this.query, {
            backwards: this.isBackwards,
            wrap: this.isWrap,
            caseSensitive: this.useCaseSensitive,
            wholeWord: this.useWholeWordSearch,
            regExp: this.useRegex,
            range: this.searchOnlyInSelection
        });

        if (this.totalCount === 0) this.isQueryNotFound = true;
    }

    public replaceEntry(event: KeyboardEvent) {
        if (this.isQueryLong || this.isQueryNotFound) return;

        let fromStr = this.findEntryElm.nativeElement.value;
        let toStr   = this.replaceEntryElm.nativeElement.value;

        if (!fromStr) return;

        this.editor.replace(toStr, fromStr, {
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
        if (this.isQueryLong || this.isQueryNotFound) return;

        let fromStr = this.findEntryElm.nativeElement.value;
        let toStr   = this.replaceEntryElm.nativeElement.value;

        if (!fromStr) return;

        this.editor.replaceAll(toStr, fromStr, {
            backwards: this.isBackwards,
            wrap: this.isWrap,
            caseSensitive: this.useCaseSensitive,
            wholeWord: this.useWholeWordSearch,
            regExp: this.useRegex,
            range: this.searchOnlyInSelection
        });

        this.isQueryNotFound = true;
    }

    public searchForString() {
        if (this.searchTimeoutId) { clearTimeout(this.searchTimeoutId); }

        this.query = this.findEntryElm.nativeElement.value;

        if (!this.query) {
            this.isQueryLong     = false;
            this.isQueryNotFound = false;

            return;
        }

        this.isQueryLong = (this.query.length > 80);
        if (this.isQueryLong) return;

        this.searchTimeoutId = setTimeout(() => {
            this.totalCount   = this.editor.findAll(this.query, {
                backwards: this.isBackwards,
                wrap: this.isWrap,
                caseSensitive: this.useCaseSensitive,
                wholeWord: this.useWholeWordSearch,
                regExp: this.useRegex,
                range: this.searchOnlyInSelection
            });

            this.isQueryNotFound = (this.totalCount === 0);
        }, this.searchTimeout);
    }

}