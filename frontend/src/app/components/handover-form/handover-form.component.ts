import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HandoverRequest } from '../../models/handover.model';

@Component({
    selector: 'app-handover-form',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './handover-form.component.html',
    styleUrls: ['./handover-form.component.css'],
})
export class HandoverFormComponent {
    @Output() generateHandover = new EventEmitter<HandoverRequest>();

    shiftNotes: string = '';
    alarmsFile: File | null = null;
    trendsFile: File | null = null;
    isLoading: boolean = false;

    onAlarmsFileChange(event: Event): void {
        const input = event.target as HTMLInputElement;
        if (input.files && input.files.length > 0) {
            this.alarmsFile = input.files[0];
        }
    }

    onTrendsFileChange(event: Event): void {
        const input = event.target as HTMLInputElement;
        if (input.files && input.files.length > 0) {
            this.trendsFile = input.files[0];
        }
    }

    async onSubmit(): Promise<void> {
        if (!this.shiftNotes.trim()) {
            alert('Please enter shift notes');
            return;
        }

        this.isLoading = true;

        try {
            const request: HandoverRequest = {
                shiftNotes: this.shiftNotes,
            };

            // Read alarms JSON file
            if (this.alarmsFile) {
                const alarmsText = await this.readFileAsText(this.alarmsFile);
                try {
                    request.alarmsJson = JSON.parse(alarmsText);
                } catch (e) {
                    console.error('Invalid JSON in alarms file:', e);
                    alert('Alarms file contains invalid JSON');
                    this.isLoading = false;
                    return;
                }
            }

            // Read trends CSV file
            if (this.trendsFile) {
                request.trendsCsv = await this.readFileAsText(this.trendsFile);
            }

            this.generateHandover.emit(request);
        } catch (error) {
            console.error('Error reading files:', error);
            alert('Error reading uploaded files');
            this.isLoading = false;
        }
    }

    private readFileAsText(file: File): Promise<string> {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target?.result as string);
            reader.onerror = (e) => reject(e);
            reader.readAsText(file);
        });
    }

    setLoading(loading: boolean): void {
        this.isLoading = loading;
    }

    loadSampleData(sampleNumber: number): void {
        const samples = [
            {
                notes: `Day Shift Handover - Jan 7, 2026

Reactor R-101: Operating at 95% capacity. Temperature stable at 385°C.
Pressure holding at 22 bar. No issues.

Compressor C-202: Started vibration alarm around 14:30. Checked bearing temps - all normal.
Vibration reduced after adjusting discharge valve. Monitor closely.

Tank T-303: Level at 78%. Normal operations. Scheduled for cleaning next week.

Distillation Column D-401: Feed rate reduced to 85% due to upstream maintenance.
Column pressure fluctuating between 1.2-1.5 bar. Keep an eye on this.

Power outage from 10:15-10:45. All equipment restarted successfully on UPS.
Some minor alarm flooding but everything back to normal now.

Night shift: Please monitor C-202 vibration and D-401 pressure closely.`,
                alarms: null,
                trends: null,
            },
            {
                notes: `Night Shift Report - Jan 7, 2026

Critical: Pump P-105 failed at 02:15. Backup pump P-106 automatically engaged.
Maintenance notified. P-105 has been showing bearing wear for 2 days.

Heat Exchanger HX-201: Fouling detected. Outlet temp dropped from 120°C to 105°C.
Cleaning scheduled for day shift. Reduced throughput by 10% to compensate.

Alarms: High level alarm on separator S-301 at 03:45. Operator manually drained.
Root cause: Level controller LIC-301 drift. Needs calibration.

Tank Farm: All tanks within normal levels. T-501 at 92% - arrange transfer to T-502.

Production:
- Throughput: 850 tons (target: 900 tons) - reduced due to HX-201 fouling
- Quality: All within spec
- Downtime: 30 min for P-105 switchover

Day shift priorities:
1. Calibrate LIC-301
2. Investigate P-105 failure
3. Monitor HX-201 performance
4. Transfer from T-501 to T-502`,
                alarms: {
                    active: [
                        {
                            id: 'LIC-301-HI',
                            tag: 'S-301.Level',
                            priority: 'High',
                            timestamp: '2026-01-07T03:45:00Z',
                        },
                    ],
                },
                trends: null,
            },
            {
                notes: `Evening Shift Update - Jan 7, 2026

Reactor Train A: Normal operation. All parameters in range.

Reactor Train B: Started trip sequence at 18:20 due to high pressure alarm PIC-405.
Investigation shows pressure transmitter fault (PT-405).
Reactor safely shut down. Estimated restart: 4 hours after transmitter replacement.

Impact: Production reduced by 50%. Customer order #C2401 may be delayed.

Compressor Package: Running at higher load (110%) to compensate for Train B shutdown.
Discharge temperature elevated to 95°C (normal: 85°C). Within acceptable limits but monitor.

Storage: Product tanks adequate for 18 hours at current rate.

Maintenance: PT-405 replacement in progress. ETA 22:00.

Night shift actions:
1. Monitor compressor temperatures closely
2. Restart Train B after PT-405 replacement (follow SOP-405-R)
3. Notify production planning of potential delay
4. Check product tank levels every 2 hours

Open questions:
- Was PT-405 recently calibrated? Check maintenance history.
- Do we have spare transmitters for other critical loops?`,
                alarms: {
                    active: [
                        {
                            id: 'PIC-405-HI',
                            tag: 'Reactor-B.Pressure',
                            priority: 'Critical',
                            timestamp: '2026-01-07T18:20:00Z',
                            value: 28.5,
                            setpoint: 25,
                        },
                    ],
                },
                trends: `timestamp,tag,value,unit
2026-01-07T18:00:00Z,Compressor.DischTemp,85,°C
2026-01-07T18:15:00Z,Compressor.DischTemp,88,°C
2026-01-07T18:20:00Z,Compressor.DischTemp,92,°C
2026-01-07T18:25:00Z,Compressor.DischTemp,95,°C
2026-01-07T18:30:00Z,Compressor.DischTemp,95,°C`,
            },
        ];

        if (sampleNumber >= 1 && sampleNumber <= 3) {
            const sample = samples[sampleNumber - 1];
            this.shiftNotes = sample.notes;
            // Note: For demo, we're just setting the text. In real app, you'd need to create File objects
            // which is more complex. Users can manually upload the JSON/CSV files from sample-data folder.
        }
    }
}
