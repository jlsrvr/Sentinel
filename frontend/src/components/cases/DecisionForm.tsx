import { useState } from 'react';
import { useTimer } from '../../hooks/useTimer';
import { useSubmitDecision } from '../../hooks/useCases';

const ACTIONS = [
    { value: 'approve', label: 'Approve' },
    { value: 'remove', label: 'Remove' },
    { value: 'warn', label: 'Warn' },
    { value: 'restrict', label: 'Restrict' },
    { value: 'escalate', label: 'Escalate' },
    { value: 'request_info', label: 'Request info' },
];

const CONFIDENCE_LEVELS = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
];

function formatTime(seconds: number): string {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
}

interface DecisionFormProps {
    caseId: string;
}

export function DecisionForm({ caseId }: DecisionFormProps) {
    const seconds = useTimer();
    const { mutate: submitDecision, isPending } = useSubmitDecision(caseId);

    const [action, setAction] = useState('');
    const [confidence, setConfidence] = useState('');
    const [rationale, setRationale] = useState('');
    const [policyReference, setPolicyReference] = useState('');

    const isValid = action !== '' && confidence !== '' && rationale.trim() !== '';

    function handleSubmit() {
        if (!isValid) return;
        submitDecision({
            action,
            confidence,
            rationale: rationale.trim(),
            policy_reference: policyReference.trim() || null,
            time_on_case_secs: seconds,
        }, {
            onSuccess: () => {
                setAction('');
                setConfidence('');
                setRationale('');
                setPolicyReference('');
            }
        });
    }

    return (
        <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
            <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
                <span className="text-[11px] uppercase tracking-widest text-gray-400 font-medium">
                    Submit decision
                </span>
                <span className="text-xs font-mono text-gray-400 tabular-nums">
                    ⏱ {formatTime(seconds)}
                </span>
            </div>

            <div className="px-5 py-4 space-y-4">
                <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                        <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                            Action <span className="text-red-500">*</span>
                        </label>
                        <select
                            value={action}
                            onChange={e => setAction(e.target.value)}
                            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Select action</option>
                            {ACTIONS.map(a => (
                                <option key={a.value} value={a.value}>{a.label}</option>
                            ))}
                        </select>
                    </div>

                    <div className="space-y-1.5">
                        <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                            Confidence <span className="text-red-500">*</span>
                        </label>
                        <select
                            value={confidence}
                            onChange={e => setConfidence(e.target.value)}
                            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Select confidence</option>
                            {CONFIDENCE_LEVELS.map(c => (
                                <option key={c.value} value={c.value}>{c.label}</option>
                            ))}
                        </select>
                    </div>
                </div>

                <div className="space-y-1.5">
                    <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                        Rationale <span className="text-red-500">*</span>
                    </label>
                    <textarea
                        value={rationale}
                        onChange={e => setRationale(e.target.value)}
                        placeholder="Explain your reasoning..."
                        rows={4}
                        className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                    />
                </div>

                <div className="space-y-1.5">
                    <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                        Policy reference
                        <span className="ml-1 text-gray-400 normal-case font-normal tracking-normal">optional</span>
                    </label>
                    <input
                        type="text"
                        value={policyReference}
                        onChange={e => setPolicyReference(e.target.value)}
                        placeholder="e.g. ToS 4.2 — Harassment"
                        className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>

                <div className="flex items-center justify-between pt-1">
                    <span className="text-xs text-gray-400">
                        Time on case: <span className="font-mono">{formatTime(seconds)}</span>
                    </span>
                    <button
                        onClick={handleSubmit}
                        disabled={!isValid || isPending}
                        className="px-4 py-2 text-sm font-medium bg-gray-900 text-white rounded-lg hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                    >
                        {isPending ? 'Submitting...' : 'Submit decision'}
                    </button>
                </div>
            </div>
        </div>
    );
}