export interface CriticalAlarm {
    alarm: string;
    meaning: string;
}

export interface OpenIssue {
    issue: string;
    priority: 'High' | 'Med' | 'Low';
    confidence: number;
}

export interface HandoverStructured {
    shiftSummary: string[];
    criticalAlarms: CriticalAlarm[];
    openIssues: OpenIssue[];
    recommendedActions: string[];
    questions: string[];
}

export interface HandoverRequest {
    shiftNotes: string;
    alarmsJson?: any;
    trendsCsv?: string;
}

export interface HandoverResponse {
    markdown: string;
    json: HandoverStructured;
    sessionId?: string;
}
