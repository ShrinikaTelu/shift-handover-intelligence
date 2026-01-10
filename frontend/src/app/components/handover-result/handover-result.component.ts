import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { HandoverResponse } from '../../models/handover.model';

@Component({
    selector: 'app-handover-result',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './handover-result.component.html',
    styleUrls: ['./handover-result.component.css'],
})
export class HandoverResultComponent {
    @Input() result: HandoverResponse | null = null;
    @Input() error: string | null = null;

    constructor(private sanitizer: DomSanitizer) {}

    copyToClipboard(): void {
        if (!this.result?.markdown) return;

        navigator.clipboard.writeText(this.result.markdown).then(
            () => {
                alert('✅ Handover copied to clipboard!');
            },
            (err) => {
                console.error('Failed to copy:', err);
                alert('❌ Failed to copy to clipboard');
            }
        );
    }

    getRenderedMarkdown(): SafeHtml {
        if (!this.result?.markdown) return '';

        // Convert markdown to HTML
        let html = this.result.markdown;

        // Headers
        html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
        html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
        html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

        // Bold
        html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');

        // Italic
        html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');

        // Lists
        html = html.replace(/^\* (.+)$/gim, '<li>$1</li>');
        html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

        // Numbered lists
        html = html.replace(/^\d+\.\s+(.+)$/gim, '<li>$1</li>');

        // Tables
        html = this.convertMarkdownTables(html);

        // Paragraphs
        html = html.replace(/\n\n/g, '</p><p>');
        html = '<p>' + html + '</p>';

        // Clean up empty paragraphs
        html = html.replace(/<p><\/p>/g, '');
        html = html.replace(/<p>(<h[1-6]>)/g, '$1');
        html = html.replace(/(<\/h[1-6]>)<\/p>/g, '$1');
        html = html.replace(/<p>(<ul>)/g, '$1');
        html = html.replace(/(<\/ul>)<\/p>/g, '$1');
        html = html.replace(/<p>(<table>)/g, '$1');
        html = html.replace(/(<\/table>)<\/p>/g, '$1');

        return this.sanitizer.sanitize(1, html) || '';
    }

    private convertMarkdownTables(text: string): string {
        const lines = text.split('\n');
        let result: string[] = [];
        let inTable = false;
        let tableRows: string[] = [];

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();

            if (line.startsWith('|') && line.endsWith('|')) {
                if (!inTable) {
                    inTable = true;
                    tableRows = [];
                }
                tableRows.push(line);

                // Check if next line is separator
                if (i + 1 < lines.length && lines[i + 1].includes('---')) {
                    i++; // Skip separator line
                }
            } else {
                if (inTable) {
                    result.push(this.tableToHtml(tableRows));
                    inTable = false;
                    tableRows = [];
                }
                result.push(line);
            }
        }

        if (inTable) {
            result.push(this.tableToHtml(tableRows));
        }

        return result.join('\n');
    }

    private tableToHtml(rows: string[]): string {
        if (rows.length === 0) return '';

        const parseRow = (row: string) =>
            row
                .split('|')
                .slice(1, -1)
                .map((cell) => cell.trim());

        const headerCells = parseRow(rows[0]);
        const header =
            '<thead><tr>' +
            headerCells.map((cell) => `<th>${cell}</th>`).join('') +
            '</tr></thead>';

        const bodyRows = rows.slice(1);
        const body =
            '<tbody>' +
            bodyRows
                .map((row) => {
                    const cells = parseRow(row);
                    return (
                        '<tr>' +
                        cells.map((cell) => `<td>${cell}</td>`).join('') +
                        '</tr>'
                    );
                })
                .join('') +
            '</tbody>';

        return `<table>${header}${body}</table>`;
    }

    getPriorityClass(priority: string): string {
        const classes: { [key: string]: string } = {
            High: 'priority-high',
            Med: 'priority-med',
            Low: 'priority-low',
        };
        return classes[priority] || 'priority-med';
    }

    getPriorityEmoji(priority: string): string {
        const emojis: { [key: string]: string } = {
            High: '🔴',
            Med: '🟡',
            Low: '🟢',
        };
        return emojis[priority] || '⚪';
    }

    getConfidenceClass(confidence: number): string {
        if (confidence >= 80) return 'confidence-high';
        if (confidence >= 50) return 'confidence-med';
        return 'confidence-low';
    }

    downloadMarkdown(): void {
        if (!this.result?.markdown) return;

        const blob = new Blob([this.result.markdown], {
            type: 'text/markdown',
        });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `shift-handover-${new Date()
            .toISOString()
            .slice(0, 10)}.md`;
        link.click();
        window.URL.revokeObjectURL(url);
    }
}
