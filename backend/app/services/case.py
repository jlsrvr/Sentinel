import uuid
from datetime import datetime
from app.models.enums import CaseStatus
from app.models.case import Case
from app.core.exceptions import InvalidTransitionError

VALID_TRANSITIONS: dict[CaseStatus, set[CaseStatus]] = {
    CaseStatus.UNASSIGNED: {CaseStatus.ASSIGNED},
    CaseStatus.ASSIGNED: {CaseStatus.IN_REVIEW},
    CaseStatus.IN_REVIEW: {CaseStatus.RESOLVED, CaseStatus.ESCALATED},
    CaseStatus.ESCALATED: {CaseStatus.ASSIGNED, CaseStatus.RESOLVED},
}

TRANSITION_SIDE_EFFECTS: dict[CaseStatus, callable] = {
    CaseStatus.ASSIGNED: lambda case: setattr(case, 'assigned_at', datetime.now()),
    CaseStatus.RESOLVED: lambda case: setattr(case, 'resolved_at', datetime.now()),
}

def can_transition(current : CaseStatus, target : CaseStatus):
    valid_targets = VALID_TRANSITIONS.get(current, set())
    return target in valid_targets

def transition(case: Case, target_status: CaseStatus):
    if not can_transition(case.status, target_status):
        raise InvalidTransitionError(case.status, target_status)
    case.status = target_status
    side_effect = TRANSITION_SIDE_EFFECTS.get(target_status)
    if side_effect:
        side_effect(case)

def assign(case: Case, reviewer_id: uuid.UUID):
    transition(case, CaseStatus.ASSIGNED)
    case.assigned_to = reviewer_id