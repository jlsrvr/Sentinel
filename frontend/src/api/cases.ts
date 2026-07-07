import type { Case } from "../types/case";
import type { Decision } from "../types/decision";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function fetchCases(skip: number = 0, limit: number = 20): Promise<Case[]> {
    const response = await fetch(`${BASE_URL}/api/v1/cases/?skip=${skip}&limit=${limit}`);
    if (!response.ok) {
        throw new Error("Failed to fetch cases");
    }
    const data = await response.json();
    return data as Case[];
}

async function fetchCase(id: string): Promise<Case> {
    const response = await fetch(`${BASE_URL}/api/v1/cases/${id}`);
    if (!response.ok) {
        throw new Error("Failed to fetch case");
    }
    const data = await response.json();
    return data as Case;
}

async function fetchDecisions(caseId: string): Promise<Decision[]> {
    const response = await fetch(`${BASE_URL}/api/v1/cases/${caseId}/decisions/`);
    if (!response.ok) {
        throw new Error("Failed to fetch decisions");
    }
    const data = await response.json();
    return data as Decision[];
}

async function assignCase(caseId: string): Promise<void> {
    const response = await fetch(`${BASE_URL}/api/v1/cases/${caseId}/assign`, {
        method: 'POST'
    });
    if (!response.ok) throw new Error('Failed to assign case');
}

async function startReview(caseId: string): Promise<void> {
    const response = await fetch(`${BASE_URL}/api/v1/cases/${caseId}/start-review`, {
        method: 'POST'
    });
    if (!response.ok) throw new Error('Failed to start review');
}

async function submitDecision(caseId: string, body: {
    action: string;
    confidence: string;
    rationale: string;
    policy_reference: string | null;
    time_on_case_secs: number;
}): Promise<void> {
    const response = await fetch(`${BASE_URL}/api/v1/cases/${caseId}/decisions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error('Failed to submit decision');
}

export { fetchCases, fetchCase, fetchDecisions, assignCase, startReview, submitDecision };