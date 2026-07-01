from app.models.enums import CaseStatus
from app.models.case import Case
from app.core.exceptions import InvalidTransitionError

VALID_TRANSITIONS: dict[CaseStatus, set[CaseStatus]] = {
    CaseStatus.UNASSIGNED: {CaseStatus.ASSIGNED},
    CaseStatus.ASSIGNED: {CaseStatus.IN_REVIEW},
    CaseStatus.IN_REVIEW: {CaseStatus.RESOLVED, CaseStatus.ESCALATED},
    CaseStatus.ESCALATED: {CaseStatus.ASSIGNED, CaseStatus.RESOLVED},
}

def can_transition(current : CaseStatus, target : CaseStatus):
    valid_targets = VALID_TRANSITIONS.get(current, set())
    return target in valid_targets

def transition(case : Case, target_status: CaseStatus):
    if can_transition(case.status, target_status):
        case.status = target_status
    else:
        raise InvalidTransitionError(case.status, target_status)