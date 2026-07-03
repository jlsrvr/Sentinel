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
    sla_deadline: string | null;
}