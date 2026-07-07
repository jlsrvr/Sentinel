import { useParams, useNavigate } from 'react-router-dom';
import { useAssignCase, useCase, useDecisions } from '../hooks/useCases';
import { formatLabel } from '../utils/format';
import type { Severity, CaseStatus } from '../types/case';


const SEVERITY_PILL: Record<Severity, string> = {
    critical: 'bg-red-100 text-red-800',
    high: 'bg-orange-100 text-orange-800',
    medium: 'bg-blue-100 text-blue-800',
    low: 'bg-green-100 text-green-800',
};

const STATUS_PILL: Record<CaseStatus, string> = {
    unassigned: 'bg-gray-100 text-gray-700',
    assigned: 'bg-blue-100 text-blue-700',
    in_review: 'bg-emerald-100 text-emerald-700',
    escalated: 'bg-orange-100 text-orange-700',
    resolved: 'bg-green-100 text-green-700',
};

function formatDate(iso: string | null): string {
    if (!iso) return '—';
    return new Date(iso).toLocaleString('en-GB', {
        day: '2-digit', month: 'short', year: 'numeric',
        hour: '2-digit', minute: '2-digit',
    });
}

function formatSla(sla: string | null): { label: string; className: string } {
    if (!sla) return { label: '—', className: 'text-gray-400' };
    const diff = new Date(sla).getTime() - Date.now();
    const hours = Math.floor(diff / 1000 / 60 / 60);
    if (hours < 0) return { label: 'Overdue', className: 'text-red-700 font-medium' };
    if (hours < 2) return { label: `< 1h left`, className: 'text-orange-700 font-medium' };
    return { label: `${hours}h left`, className: 'text-gray-600' };
}

function DetailRow({ label, children }: { label: string; children: React.ReactNode }) {
    return (
        <tr className="border-b border-gray-50">
            <td className="py-3 pr-6 text-sm text-gray-400 font-medium w-40 align-top">{label}</td>
            <td className="py-3 text-sm text-gray-800">{children}</td>
        </tr>
    );
}

function Pill({ label, className }: { label: string; className: string }) {
    return (
        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium uppercase tracking-wide ${className}`}>
            {label}
        </span>
    );
}

export default function CaseDetailPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const { data: c, isLoading: caseLoading, error: caseError } = useCase(id!);
    const { data: decisions, isLoading: decisionsLoading } = useDecisions(id!);
    const { mutate: assignCase, isPending } = useAssignCase(id!);


    if (caseLoading) return <div className="min-h-screen bg-gray-50 p-8"><p className="text-sm text-gray-400">Loading case...</p></div>;
    if (caseError || !c) return <div className="min-h-screen bg-gray-50 p-8"><p className="text-sm text-red-600">Case not found.</p></div>;

    const sla = formatSla(c.sla_deadline);

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-3xl mx-auto space-y-6">
                <div className="flex justify-between">
                    <div className="flex items-center gap-3">
                        <button
                            onClick={() => navigate('/')}
                            className="text-sm text-gray-400 hover:text-gray-600 transition-colors"
                        >
                            ← Queue
                        </button>
                        <span className="text-gray-200">/</span>
                        <span className="text-sm text-gray-500 font-mono">{c.external_id}</span>
                    </div>
                    {
                        c.status === 'unassigned' && (
                            <button
                                onClick={() => assignCase()}
                                disabled={isPending}
                                className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                            >
                                {isPending ? 'Assigning...' : 'Take case'}
                            </button>
                        )
                    }
                </div>

                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                    <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
                        <span className="text-[11px] uppercase tracking-widest text-gray-400 font-medium">Case details</span>
                        <div className="flex gap-2">
                            <Pill label={c.severity} className={SEVERITY_PILL[c.severity]} />
                            <Pill label={c.status.replace('_', ' ')} className={STATUS_PILL[c.status]} />
                        </div>
                    </div>

                    <div className="px-5 py-2">
                        <table className="w-full">
                            <tbody>
                                <DetailRow label="Case ID">{c.external_id}</DetailRow>
                                <DetailRow label="Content type">{c.content_type}</DetailRow>
                                <DetailRow label="Source">{formatLabel(c.source)}</DetailRow>
                                {/* TODO: Replace with queue name when available */}
                                <DetailRow label="Queue">{c.queue_id}</DetailRow>
                                <DetailRow label="Assigned to">{c.assigned_to ?? '—'}</DetailRow>
                                <DetailRow label="Assigned at">{formatDate(c.assigned_at ?? null)}</DetailRow>
                                <DetailRow label="SLA deadline">
                                    <span className={sla.className}>{sla.label}</span>
                                    {c.sla_deadline && (
                                        <span className="ml-2 text-gray-400">({formatDate(c.sla_deadline)})</span>
                                    )}
                                </DetailRow>
                                <DetailRow label="Created">{formatDate(c.created_at)}</DetailRow>
                                <DetailRow label="Updated">{formatDate(c.updated_at)}</DetailRow>
                                {c.resolved_at && (
                                    <DetailRow label="Resolved">{formatDate(c.resolved_at)}</DetailRow>
                                )}
                                {c.content_snapshot && (
                                    <DetailRow label="Content">
                                        <span className="font-mono text-xs bg-gray-50 px-2 py-1 rounded border border-gray-100 block">
                                            {c.content_snapshot}
                                        </span>
                                    </DetailRow>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                    <div className="px-5 py-4 border-b border-gray-100">
                        <span className="text-[11px] uppercase tracking-widest text-gray-400 font-medium">Decision history</span>
                    </div>

                    {decisionsLoading ? (
                        <p className="px-5 py-4 text-sm text-gray-400">Loading decisions...</p>
                    ) : !decisions?.length ? (
                        <p className="px-5 py-4 text-sm text-gray-400">No decisions yet.</p>
                    ) : (
                        <table className="w-full border-collapse">
                            <thead>
                                <tr className="border-b border-gray-100">
                                    {['Action', 'Confidence', 'Policy ref', 'Time spent', 'Submitted'].map(h => (
                                        <th key={h} className="px-4 py-2.5 text-left text-[11px] uppercase tracking-widest text-gray-400 font-medium">
                                            {h}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-50">
                                {decisions.map(d => (
                                    <tr key={d.id} className="hover:bg-gray-50">
                                        <td className="px-4 py-3 text-sm font-medium text-gray-800">{d.action}</td>
                                        <td className="px-4 py-3 text-sm text-gray-500">{d.confidence}</td>
                                        <td className="px-4 py-3 text-sm text-gray-400">{d.policy_reference ?? '—'}</td>
                                        <td className="px-4 py-3 text-sm text-gray-500 tabular-nums">{Math.round(d.time_on_case_secs / 60)}m</td>
                                        <td className="px-4 py-3 text-sm text-gray-400">{formatDate(d.created_at)}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>

                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                    <div className="px-5 py-4 border-b border-gray-100">
                        <span className="text-[11px] uppercase tracking-widest text-gray-400 font-medium">Rationale</span>
                    </div>
                    {!decisions?.length ? (
                        <p className="px-5 py-4 text-sm text-gray-400">No decisions yet.</p>
                    ) : (
                        <div className="divide-y divide-gray-50">
                            {decisions.map(d => (
                                <div key={d.id} className="px-5 py-4">
                                    <div className="flex items-center gap-2 mb-1">
                                        <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">{d.action}</span>
                                        <span className="text-gray-200">·</span>
                                        <span className="text-xs text-gray-400">{formatDate(d.created_at)}</span>
                                    </div>
                                    <p className="text-sm text-gray-700 leading-relaxed">{d.rationale}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

            </div>
        </div>
    );
}