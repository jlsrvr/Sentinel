from app.models.enums import CaseStatus

VALID_TRANSITIONS: dict[CaseStatus, set[CaseStatus]] = {
    CaseStatus.UNASSIGNED: {CaseStatus.ASSIGNED},
    CaseStatus.ASSIGNED: {CaseStatus.IN_REVIEW},
    CaseStatus.IN_REVIEW: {CaseStatus.RESOLVED, CaseStatus.ESCALATED},
    CaseStatus.ESCALATED: {CaseStatus.ASSIGNED, CaseStatus.RESOLVED},
}
def can_transition(current : CaseStatus, target : CaseStatus):
    valid_targets = VALID_TRANSITIONS.get(current, set())
    return target in valid_targets