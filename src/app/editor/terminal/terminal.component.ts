import {
    Component,
    DestroyRef,
    ElementRef,
    HostBinding,
    ViewChild,
    inject
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

// import { Terminal } from 'xterm';
import { Terminal } from '@xterm/xterm';
// import { FitAddon } from 'xterm-addon-fit';

import { TerminalService } from '../../common/services/editor/terminal/terminal.service';

import { ServiceMessage } from '../../common/types/service-message.type';



@Component({
    selector: 'terminal',
    standalone: true,
    imports: [
    ],
    templateUrl: './terminal.component.html',
    styleUrl: './terminal.component.css',
    host: {
        'class': 'row terminal',
        "(keyup)": "globalTerminalKeyHandler($event)"
    }
})
export class TerminalComponent {
    readonly #destroyRef: DestroyRef               = inject(DestroyRef);

    private terminalService: TerminalService       = inject(TerminalService);
    private terminal: Terminal                     = new Terminal();

    @HostBinding("class.hidden") isHidden: boolean = true;
    @ViewChild("terminalElm") terminalElm!: ElementRef;

    private editor!: any;

    constructor() {
        this.loadSubscribers();
        this.loadMainSubscribers();
    }

    private ngAfterViewInit(): void {
        this.loadTerminal();
    }

    // Note: https://stackoverflow.com/questions/63390143/how-do-i-connect-xterm-jsin-electron-to-a-real-working-command-prompt
    private loadTerminal() {
        // const fitAddon = new FitAddon();
        // this.terminal.loadAddon(fitAddon);

        this.terminal.open(this.terminalElm.nativeElement);
        this.terminal.onData(e => {
            console.log(e);
            // ipcRenderer.send("terminal-into", e);
            // window.main.quit();
        } );

        // ipcRenderer.on('terminal-actions', (event, data) => {
        //     this.terminal.write(data);
        // })

        // Make the terminal's size and geometry fit the size of #terminal-container
        // fitAddon.fit();
    }

    private loadSubscribers() {
        this.terminalService.getMessage$().pipe(
            takeUntilDestroyed(this.#destroyRef)
        ).subscribe((message: ServiceMessage) => {
            switch ( message.action ) {
                case "toggle-terminal":
                    this.toggleTerminal(message);
                    break;
                case "set-active-editor":
                    this.setActiveEditor(message);
                    break;
                default:
                    break;
            }
        });
    }

    private loadMainSubscribers() {
        window.main.onTerminalActions(async (action: string) => {
            this.terminal.write(action);
            // switch ( action ) {
            //     case "terminal-actions":
            //         break;
            //     default:
            //         break;
            // }
        });
    }


    private toggleTerminal(message: ServiceMessage) {
        this.isHidden = !this.isHidden;

        if (this.isHidden) {
            this.editor.focus();
            return;
        }

        // setTimeout(() => {
        // }, 200);
    }


    private setActiveEditor(message: ServiceMessage) {
        if (this.editor == message.rawData) return;

        this.editor = message.rawData;

        if (this.isHidden) return;
    }

    public hideTerminal() {
        this.isHidden = true;
        this.editor.focus();
    }

    public globalTerminalKeyHandler(event: any) {
        if (event.ctrlKey && event.key === ".") {
            this.hideTerminal();
        }
    }



}