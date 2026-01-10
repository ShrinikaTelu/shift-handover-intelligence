import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { HandoverRequest, HandoverResponse } from '../models/handover.model';

@Injectable({
    providedIn: 'root',
})
export class HandoverService {
    private readonly API_URL = 'http://localhost:8000/api';

    constructor(private http: HttpClient) {}

    generateHandover(request: HandoverRequest): Observable<HandoverResponse> {
        return this.http
            .post<HandoverResponse>(
                `${this.API_URL}/handover/generate`,
                request
            )
            .pipe(catchError(this.handleError));
    }

    getHandover(sessionId: string): Observable<HandoverResponse> {
        return this.http
            .get<HandoverResponse>(`${this.API_URL}/handover/${sessionId}`)
            .pipe(catchError(this.handleError));
    }

    checkHealth(): Observable<any> {
        return this.http
            .get('http://localhost:8000/health')
            .pipe(catchError(this.handleError));
    }

    private handleError(error: HttpErrorResponse): Observable<never> {
        let errorMessage = 'An error occurred';

        if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Error: ${error.error.message}`;
        } else {
            // Server-side error
            errorMessage =
                error.error?.detail || error.message || 'Server error';
        }

        console.error('API Error:', error);
        return throwError(() => new Error(errorMessage));
    }
}
