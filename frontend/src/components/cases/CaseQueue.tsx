import { useCases } from '../../hooks/useCases';

const SEVERITY_COLORS: Record<string, string> = {
    critical: '#ef4444',
    high: '#f97316',
    medium: '#eab308',
    low: '#22c55e',
};

function formatSlaDeadline(sla: string | null): string {
    if (!sla) return '—';
    const diff = new Date(sla).getTime() - Date.now();
    const hours = Math.floor(diff / 1000 / 60 / 60);
    if (hours < 0) return 'Overdue';
    if (hours < 1) return '< 1h';
    return `${hours}h`;
}

export function CaseQueue() {
    const { data: cases, isLoading, error } = useCases();

    if (isLoading) return <p>Loading cases...</p>;
    if (error) return <p>Failed to load cases.</p>;
    if (!cases?.length) return <p>No cases in queue.</p>;

    return (
        <table>
            <thead>
                <tr>
                    <th>Severity</th>
                    <th>SLA</th>
                    <th>Status</th>
                    <th>Type</th>
                    <th>Source</th>
                </tr>
            </thead>
            <tbody>
                {cases.map((c) => (
                    <tr key={c.id}>
                        <td style={{ color: SEVERITY_COLORS[c.severity] }}>
                            {c.severity.toUpperCase()}
                        </td>
                        <td>{formatSlaDeadline(c.sla_deadline)}</td>
                        <td>{c.status}</td>
                        <td>{c.content_type}</td>
                        <td>{c.source}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}