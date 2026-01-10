import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HandoverFormComponent } from './components/handover-form/handover-form.component';
import { HandoverResultComponent } from './components/handover-result/handover-result.component';
import { HandoverService } from './services/handover.service';
import { HandoverRequest, HandoverResponse } from './models/handover.model';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, HandoverFormComponent, HandoverResultComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css',
})
export class AppComponent {
    @ViewChild(HandoverFormComponent) formComponent?: HandoverFormComponent;

    title = 'Shift Handover Intelligence';
    result: HandoverResponse | null = null;
    error: string | null = null;

    constructor(private handoverService: HandoverService) {}

    onGenerateHandover(request: HandoverRequest): void {
        this.result = null;
        this.error = null;

        this.handoverService.generateHandover(request).subscribe({
            next: (response) => {
                this.result = response;
                this.formComponent?.setLoading(false);
            },
            error: (err) => {
                this.error = err.message;
                this.formComponent?.setLoading(false);
            },
        });
    }
}
