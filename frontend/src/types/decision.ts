export type Action = "approve" | "remove" | "warn" | "restrict" | "escalate" | "request_info";
export type Confidence = 'low' | 'medium' | 'high';

export interface Decision {
    id: string;
    case_id: string;
    reviewer_id: string;
    action: Action;
    rationale: string;
    policy_reference: string | null;
    confidence: Confidence;
}