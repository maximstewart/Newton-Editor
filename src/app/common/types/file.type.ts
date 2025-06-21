import { EditSession } from 'ace-builds';


export interface NewtonFile extends File {
    fname?: string,
    path?: string,
    hash?: string,
    session?: EditSession,
}