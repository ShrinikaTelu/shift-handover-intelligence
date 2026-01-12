import { Component, Output, EventEmitter, ChangeDetectorRef } from '@angular/core';
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

    constructor(private cdr: ChangeDetectorRef) {}

    shiftNotes: string = '';
    alarmsFile: File | null = null;
    trendsFile: File | null = null;
    isLoading: boolean = false;
    
    // File upload feedback
    alarmsFileName: string = '';
    trendsFileName: string = '';

    // Voice recording properties
    isRecording: boolean = false;
    mediaRecorder: MediaRecorder | null = null;
    audioChunks: Blob[] = [];
    recordingTime: number = 0;
    recordingTimer: any = null;
    recordedAudioBlob: Blob | null = null;
    recordingAudioUrl: string = '';
    
    // Speech recognition properties
    recognition: any = null;
    isTranscribing: boolean = false;
    
    // Playback properties
    audioElement: HTMLAudioElement | null = null;
    isPlaying: boolean = false;
    isPreparing: boolean = false;
    currentTime: number = 0;
    duration: number = 0;
    progress: number = 0; // 0-100 percentage
    playbackComplete: boolean = false;
    recordingConfirmed: boolean = false;
    
    // Store original shift notes for cancel
    shiftNotesBeforeRecording: string = '';
    
    // Playback update interval
    playbackInterval: any = null;

    onAlarmsFileChange(event: Event): void {
        const input = event.target as HTMLInputElement;
        if (input.files && input.files.length > 0) {
            this.alarmsFile = input.files[0];
            this.alarmsFileName = this.alarmsFile.name;
            console.log('Alarms file selected:', this.alarmsFileName);
        }
    }

    onTrendsFileChange(event: Event): void {
        const input = event.target as HTMLInputElement;
        if (input.files && input.files.length > 0) {
            this.trendsFile = input.files[0];
            this.trendsFileName = this.trendsFile.name;
            console.log('Trends file selected:', this.trendsFileName);
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

    // Voice Recording Methods - Live Voice-to-Text
    async startRecording(): Promise<void> {
        try {
            // Save shift notes state before recording
            this.shiftNotesBeforeRecording = this.shiftNotes;
            
            // Get user media (microphone)
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // Set up MediaRecorder for audio capture
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];
            this.recordingTime = 0;
            this.isRecording = true;

            this.mediaRecorder.ondataavailable = (event: BlobEvent) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => {
                console.log('Recording stopped');
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                this.recordedAudioBlob = audioBlob;
                this.recordingAudioUrl = URL.createObjectURL(audioBlob);
                this.cdr.detectChanges();
            };

            this.mediaRecorder.start();

            // Start recording timer
            this.recordingTimer = setInterval(() => {
                this.recordingTime++;
                this.cdr.detectChanges();
            }, 1000);

            // Initialize and start speech recognition
            this.startLiveTranscription();

        } catch (error) {
            console.error('Error accessing microphone:', error);
            alert('Unable to access microphone. Please check permissions.');
        }
    }

    private startLiveTranscription(): void {
        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            console.log('Web Speech API not available');
            alert('Speech recognition not available in your browser');
            return;
        }

        this.recognition = new SpeechRecognition();
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.language = 'en-US';

        let interimTranscript = '';
        let finalTranscriptChunk = '';

        this.recognition.onstart = () => {
            console.log('Speech recognition started');
            this.isTranscribing = true;
            this.cdr.detectChanges();
        };

        this.recognition.onresult = (event: any) => {
            interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;

                if (event.results[i].isFinal) {
                    // Final result - add to shift notes
                    finalTranscriptChunk = transcript;
                    console.log('Final transcript:', transcript);
                } else {
                    // Interim result
                    interimTranscript += transcript;
                }
            }

            // Update shift notes with final text
            if (finalTranscriptChunk) {
                const textToAdd = finalTranscriptChunk + ' ';
                this.shiftNotes += textToAdd;
                finalTranscriptChunk = '';
                this.cdr.detectChanges();
            }
        };

        this.recognition.onerror = (event: any) => {
            console.error('Speech recognition error:', event.error);
        };

        this.recognition.onend = () => {
            console.log('Speech recognition ended');
            this.isTranscribing = false;
            this.cdr.detectChanges();
        };

        try {
            this.recognition.start();
        } catch (e) {
            console.error('Error starting recognition:', e);
        }
    }

    stopRecording(): void {
        if (this.mediaRecorder && this.isRecording) {
            console.log('Stopping recording...');
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            // Stop recognition
            if (this.recognition) {
                this.recognition.stop();
            }
            
            clearInterval(this.recordingTimer);

            // Stop all audio tracks
            this.mediaRecorder.stream.getTracks().forEach((track: MediaStreamTrack) => {
                track.stop();
            });
            
            this.cdr.detectChanges();
        }
    }

    cancelRecording(): void {
        // HARD STOP: Immediately stop all audio playback
        if (this.audioElement) {
            this.audioElement.pause();
            this.audioElement.currentTime = 0;
            this.audioElement = null;
        }
        
        // Stop recording if in progress
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            if (this.recognition) {
                this.recognition.stop();
            }
            
            clearInterval(this.recordingTimer);
            
            this.mediaRecorder.stream.getTracks().forEach((track: MediaStreamTrack) => {
                track.stop();
            });
        }
        
        // Stop playback updater
        this.stopPlaybackUpdater();
        
        // Clean up audio URL
        if (this.recordingAudioUrl) {
            URL.revokeObjectURL(this.recordingAudioUrl);
            this.recordingAudioUrl = '';
        }
        
        // Restore shift notes to state before recording started
        this.shiftNotes = this.shiftNotesBeforeRecording;
        
        // Reset all recording and playback state
        this.recordedAudioBlob = null;
        this.recordingTime = 0;
        this.isTranscribing = false;
        this.isPlaying = false;
        this.isPreparing = false;
        this.currentTime = 0;
        this.duration = 0;
        this.progress = 0;
        this.playbackComplete = false;
        this.recordingConfirmed = false;
        
        this.cdr.detectChanges();
    }

    playRecording(): void {
        if (!this.audioElement && this.recordingAudioUrl) {
            this.audioElement = new Audio(this.recordingAudioUrl);
            this.isPreparing = true;
            this.cdr.detectChanges();

            // When metadata is loaded, get duration
            this.audioElement.onloadedmetadata = () => {
                this.duration = this.audioElement!.duration;
                this.isPreparing = false;
                this.cdr.detectChanges();
            };

            // When audio starts playing
            this.audioElement.onplay = () => {
                this.isPlaying = true;
                this.playbackComplete = false;
                this.cdr.detectChanges();
                this.startPlaybackUpdater();
            };

            // When audio pauses
            this.audioElement.onpause = () => {
                this.isPlaying = false;
                this.cdr.detectChanges();
            };

            // When audio ends
            this.audioElement.onended = () => {
                this.isPlaying = false;
                this.playbackComplete = true;
                this.stopPlaybackUpdater();
                this.cdr.detectChanges();
            };

            // Update current time and progress
            this.audioElement.ontimeupdate = () => {
                this.currentTime = this.audioElement!.currentTime;
                this.progress = (this.currentTime / this.duration) * 100;
                this.cdr.detectChanges();
            };
        }

        if (this.audioElement) {
            this.audioElement.play().catch(err => console.error('Playback error:', err));
        }
    }

    togglePlayPause(): void {
        // First Play: Initialize audio element if not already done
        if (!this.audioElement && this.recordingAudioUrl) {
            this.playRecording();
            return; // playRecording() will handle the play() call
        }

        // Subsequent clicks: Toggle play/pause
        if (this.audioElement) {
            if (this.isPlaying) {
                this.audioElement.pause();
            } else {
                this.audioElement.play().catch(err => console.error('Playback error:', err));
            }
        }
    }

    replayRecording(): void {
        // If audio element doesn't exist, create it first
        if (!this.audioElement && this.recordingAudioUrl) {
            this.playRecording(); // Initialize audio element and start playback
        } else if (this.audioElement) {
            // Reset to beginning and play
            this.audioElement.currentTime = 0;
            this.playbackComplete = false;
            this.cdr.detectChanges();
            this.audioElement.play().catch(err => console.error('Playback error:', err));
        }
    }

    onProgressBarClick(event: MouseEvent): void {
        if (!this.audioElement || !this.duration) return;

        const progressBar = event.target as HTMLElement;
        const rect = progressBar.getBoundingClientRect();
        const clickX = event.clientX - rect.left;
        const percentage = clickX / rect.width;
        const newTime = percentage * this.duration;

        this.audioElement.currentTime = Math.max(0, Math.min(newTime, this.duration));
        this.currentTime = this.audioElement.currentTime;
        this.progress = (this.currentTime / this.duration) * 100;
        this.cdr.detectChanges();
    }

    private startPlaybackUpdater(): void {
        if (this.playbackInterval) {
            clearInterval(this.playbackInterval);
        }
        this.playbackInterval = setInterval(() => {
            if (this.audioElement && this.isPlaying) {
                this.currentTime = this.audioElement.currentTime;
                this.progress = (this.currentTime / this.duration) * 100;
                this.cdr.detectChanges();
            }
        }, 100);
    }

    private stopPlaybackUpdater(): void {
        if (this.playbackInterval) {
            clearInterval(this.playbackInterval);
            this.playbackInterval = null;
        }
    }

    confirmRecording(): void {
        this.recordingConfirmed = true;
        this.stopPlaybackUpdater();
        if (this.audioElement) {
            this.audioElement.pause();
        }
        this.cdr.detectChanges();
    }

    clearRecording(): void {
        // Clean up playback
        this.stopPlaybackUpdater();
        if (this.audioElement) {
            this.audioElement.pause();
            this.audioElement = null;
        }

        // Clean up audio URL
        if (this.recordingAudioUrl) {
            URL.revokeObjectURL(this.recordingAudioUrl);
            this.recordingAudioUrl = '';
        }
        
        this.recordedAudioBlob = null;
        this.recordingTime = 0;
        this.audioChunks = [];
        this.isPlaying = false;
        this.isPreparing = false;
        this.currentTime = 0;
        this.duration = 0;
        this.progress = 0;
        this.playbackComplete = false;
        this.recordingConfirmed = false;
        
        this.cdr.detectChanges();
    }

    formatTime(seconds: number): string {
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
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
