import { Component, ElementRef, ViewChild, TemplateRef, ComponentRef, ViewContainerRef } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

import { TabComponent } from './tab/tab.component';
import { TabsService } from '../../common/services/editor/tabs/tabs.service';

import { ServiceMessage } from '../../common/types/service-message.type';



@Component({
    selector: 'tabs',
    standalone: true,
    imports: [
    ],
    templateUrl: './tabs.component.html',
    styleUrl: './tabs.component.css',
    host: {
        'class': 'tabs scroller'
    }
})
export class TabsComponent {
    private unsubscribe = new Subject<void>();

    @ViewChild('containerRef', {read: ViewContainerRef}) containerRef!: ViewContainerRef;
    tabs: Map<string, ComponentRef<TabComponent>>;
    activeTab!: string;


    constructor(private tabsService: TabsService) {
        this.tabs = new Map<string, ComponentRef<TabComponent>>();
    }


    public ngAfterViewInit(): void {
        this.tabsService.getData$().pipe(
            takeUntil(this.unsubscribe)
        ).subscribe((data: ServiceMessage) => {
            if (data.action === "create-tab")
                this.createTab(data.message, data.uuid, data.data);
        });
    }

    ngOnDestroy() {
        this.unsubscribe.next();
        this.unsubscribe.complete();
    }

    private createTab(title: string, uuid: string, path: string) {
        const component = this.containerRef.createComponent(TabComponent);
        component.instance.title = title;
        component.instance.path  = path;
        component.instance.ref   = component;

        this.tabs.set(uuid, component)

        return component;
    }

}