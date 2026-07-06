export type CaseStatus = "unassigned" | "assigned" | "in_review" | "escalated" | "resolved";
export type Severity = 'low' | 'medium' | 'high' | 'critical';
export type ContentType = 'text' | 'image' | 'video' | 'audio' | 'account';

export interface Case {
    id: string;
    external_id: string;
    severity: Severity;
    status: CaseStatus;
    content_type: ContentType;
    source: string;
    queue_id: string;
    assigned_to: string | null;
    assigned_at: string | null;
    content_snapshot: string | null;
    created_at: string;
    updated_at: string;
    resolved_at: string | null;
    sla_deadline: string | null;
}