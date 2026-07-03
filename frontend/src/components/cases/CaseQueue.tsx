import { useCases } from '../../hooks/useCases';
import type { Case, Severity, CaseStatus } from '../../types/case';

const SEVERITY_PILL: Record<Severity, string> = {
    critical: 'bg-red-100 text-red-800',
    high: 'bg-orange-100 text-orange-800',
    medium: 'bg-blue-100 text-blue-800',
    low: 'bg-green-100 text-green-800',
};

const STATUS_DOT: Record<CaseStatus, string> = {
    unassigned: 'bg-gray-400',
    assigned: 'bg-blue-500',
    in_review: 'bg-emerald-500',
    escalated: 'bg-orange-500',
    resolved: 'bg-gray-300',
};

function formatSla(sla: string | null): { label: string; className: string } {
    if (!sla) return { label: '—', className: 'text-gray-400' };
    const diff = new Date(sla).getTime() - Date.now();
    const hours = Math.floor(diff / 1000 / 60 / 60);
    if (hours < 0) return { label: 'Overdue', className: 'text-red-700 font-medium' };
    if (hours < 2) return { label: '< 1h', className: 'text-orange-700 font-medium' };
    return { label: `${hours}h`, className: 'text-gray-500' };
}

function SummaryCard({ label, value, danger }: { label: string; value: number; danger?: boolean }) {
    return (
        <div className="flex flex-col gap-0.5">
            <span className="text-[11px] uppercase tracking-widest text-gray-400 font-medium">{label}</span>
            <span className={`text-xl font-medium ${danger && value > 0 ? 'text-red-700' : 'text-gray-900'}`}>
                {value}
            </span>
        </div>
    );
}

function CaseRow({ c }: { c: Case }) {
    const sla = formatSla(c.sla_deadline);
    return (
        <tr className="hover:bg-gray-50 cursor-pointer transition-colors">
            <td className="px-4 py-3">
                <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium uppercase tracking-wide ${SEVERITY_PILL[c.severity]}`}>
                    {c.severity}
                </span>
            </td>
            <td className={`px-4 py-3 text-sm tabular-nums ${sla.className}`}>
                {sla.label === 'Overdue' && (
                    <span className="mr-1">⚠</span>
                )}
                {sla.label}
            </td>
            <td className="px-4 py-3">
                <span className="inline-flex items-center gap-1.5 text-sm text-gray-600">
                    <span className={`w-1.5 h-1.5 rounded-full ${STATUS_DOT[c.status]}`} />
                    {c.status.replace('_', ' ')}
                </span>
            </td>
            <td className="px-4 py-3 text-sm text-gray-400">{c.content_type}</td>
            <td className="px-4 py-3 text-sm text-gray-400">{c.source}</td>
        </tr>
    );
}

export function CaseQueue() {
    const { data: cases, isLoading, error } = useCases();

    if (isLoading) return <p className="p-6 text-sm text-gray-400">Loading cases...</p>;
    if (error) return <p className="p-6 text-sm text-red-600">Failed to load cases.</p>;
    if (!cases?.length) return <p className="p-6 text-sm text-gray-400">No cases in queue.</p>;

    const overdue = cases.filter(c => c.sla_deadline && new Date(c.sla_deadline) < new Date()).length;
    const critical = cases.filter(c => c.severity === 'critical').length;
    const unassigned = cases.filter(c => c.status === 'unassigned').length;

    return (
        <div className="border border-gray-200 rounded-xl overflow-hidden bg-white">
            <div className="flex items-center justify-between px-5 py-4 border-b border-gray-100">
                <span className="text-[11px] uppercase tracking-widest text-gray-400 font-medium">Case queue</span>
                <button className="text-xs text-gray-400 hover:text-gray-600 transition-colors">↻ Refresh</button>
            </div>

            <div className="flex gap-8 px-5 py-4 border-b border-gray-100">
                <SummaryCard label="Total" value={cases.length} />
                <SummaryCard label="Overdue" value={overdue} danger />
                <SummaryCard label="Critical" value={critical} />
                <SummaryCard label="Unassigned" value={unassigned} />
            </div>

            <table className="w-full border-collapse">
                <thead>
                    <tr className="border-b border-gray-100">
                        {['Severity', 'SLA', 'Status', 'Type', 'Source'].map(h => (
                            <th key={h} className="px-4 py-2.5 text-left text-[11px] uppercase tracking-widest text-gray-400 font-medium">
                                {h}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                    {cases.map(c => <CaseRow key={c.id} c={c} />)}
                </tbody>
            </table>
        </div>
    );
}