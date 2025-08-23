import { Injectable } from '@angular/core';

import * as ace from "ace-builds/src-min-noconflict/ace";



@Injectable({
    providedIn: 'root'
})
export class ColorTokenizerService {
    readonly #RULES: {} = {
        start: [
            { token: "hex3", regex: "#[A-Fa-f0-9]{3}(?![A-Fa-f0-9])" },
            { token: "hex6", regex: "#[A-Fa-f0-9]{6}(?![A-Fa-f0-9])" },
            { token: "hex8", regex: "#[A-Fa-f0-9]{8}(?![A-Fa-f0-9])" },
            {
                token: "rgb",
                regex: /rgb\s*\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)/
            },
            {
                token: "rgba",
                regex: /rgba\s*\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(?:0(?:\.\d+)?|1(?:\.0+)?)\s*\)/
            }
        ]
    };

    tokenizer!: any;
    cssLines: {} = {};


    constructor() {
        Object.freeze(this.#RULES)

        const Tokenizer = ace.require("ace/tokenizer").Tokenizer;
        this.tokenizer  = new Tokenizer(this.#RULES);
    }


    public async parse(data: string) {
        const lines = data.split("\n");
        for (let i = 0; i < lines.length; i++) {
            const token = this.parseLine( lines[i] );
            if (!token) continue;
            this.cssLines[i] = token;
            this.cssLines[i]["hash"] = btoa(
                token["value"]
            );
        }

        console.log(this.cssLines);
    }

    public parseLine(line: string): {} | null {
        const tokens = this.tokenizer.getLineTokens(line, "start").tokens;

        for (let i = 0; i < tokens.length; i++) {
            if ("text" === tokens[i]["type"]) continue;
            return tokens[i];
        }

        return null;
    }

}