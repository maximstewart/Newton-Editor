import { Keybindings } from './keybindings.config';

export const EditorSettings: any = {
    // BASE_PATH: 'https:cdnjs.cloudflare.com/ajax/libs/ace/1.40.1/',
    BASE_PATH: 'ace',
    KEYBINDINGS: Keybindings,
    CONFIG: {
        behavioursEnabled: true,
        fontSize: "12px",
        theme: "ace/theme/one_dark",
        mode: "ace/mode/text",
        printMarginColumn: 80,
        enableBasicAutocompletion: true,
        enableLiveAutocompletion: true,
        enableSnippets: true,
        highlightActiveLine: true,
        enableMultiselect: true,
        tabSize: 4,
        useSoftTabs: true,
        tooltipFollowsMouse: true,
        wrapBehavioursEnabled: false,
        scrollPastEnd: 0.5,
        mergeUndoDeltas: false,
        showGutter: true,
        customScrollbar: true,
        navigateWithinSoftTabs: true,
        scrollSpeed: 5
    }
};