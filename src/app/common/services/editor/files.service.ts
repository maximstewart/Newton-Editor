import { Injectable, inject } from '@angular/core';
import { ReplaySubject, Observable } from 'rxjs';

import { EditSession } from 'ace-builds';
import { getModeForPath } from 'ace-builds/src-noconflict/ext-modelist';

import { TabsService } from './tabs/tabs.service';

import { NewtonFile } from '../../types/file.type';
import { ServiceMessage } from '../../types/service-message.type';



@Injectable({
    providedIn: 'root'
})
export class FilesService {
    private messageSubject: ReplaySubject<ServiceMessage> = new ReplaySubject<ServiceMessage>(1);

    private tabsService: TabsService = inject(TabsService);

    files: Map<string, NewtonFile>;


    constructor() {
        this.files = new Map<string, NewtonFile>();
    }


    public get(path: string): NewtonFile {
        return this.files.get(path);
    }

    public delete(file: NewtonFile) {
        file.session.destroy();
        window.fs.closeFile(file.path);
        this.files.delete(file.path);
    }

    public set(file: NewtonFile) {
        this.files.set(file.path, file);
    }

    public sendMessage(data: ServiceMessage): void {
        this.messageSubject.next(data);
    }

    public getMessage$(): Observable<ServiceMessage> {
        return this.messageSubject.asObservable();
    }

    public async loadFilesList(
        files: Array<NewtonFile>
    ): Promise<NewtonFile | undefined | null> {
	    for (let i = 0; i < files.length; i++) {
		    const file = files[i];
		    const path = window.fs.getPathForFile(file);

		    if (!file || !path) continue;
		    if ( this.files.get(path) ) continue;

		    await this.addFile(path, file);
		    this.addTab(file);
	    }

	    return files[ files.length - 1 ];
    }

    public async addFile(
        path: string,
        file: NewtonFile,
        loadFileContents: boolean = true,
        data: string = ""
    ): Promise<void> {
	    try {
	        let pathParts = path.split("/");
	        file.fname    = pathParts[ pathParts.length - 1 ];
	        file.path     = path;
	        file.hash     = btoa(file.path);

	        if (loadFileContents)
	            data = await window.fs.getFileContents(file.path);

            file.session = new EditSession(data);
            file.session.setMode(
                getModeForPath( file.path ).mode
            );
            
            this.files.set(file.path, file);
	    } catch (error) {
		    console.log(
		        `----  Error  ----\nPath: ${path}\nMessage: ${error}`
		    );
	    }
    }

    public async addTab(file: NewtonFile) {
        let message      = new ServiceMessage();
        message.action   = "create-tab";
        message.fileName = file.fname;
        message.fileUUID = file.hash;
        message.filePath = file.path;

        this.tabsService.sendMessage(message);
    }


}