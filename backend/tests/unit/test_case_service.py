from app.models.enums import CaseStatus
from app.services.case import can_transition

def test_unassigned_can_transition_to_assigned():
    assert can_transition(CaseStatus.UNASSIGNED, CaseStatus.ASSIGNED) is True

def test_assigned_can_transition_to_in_review():
    assert can_transition(CaseStatus.ASSIGNED, CaseStatus.IN_REVIEW) is True

def test_in_review_can_transition_to_resolved():
    assert can_transition(CaseStatus.IN_REVIEW, CaseStatus.RESOLVED) is True

def test_escalated_can_transition_to_assigned():
    assert can_transition(CaseStatus.ESCALATED, CaseStatus.ASSIGNED) is True

def test_escalated_can_transition_to_resolved():
    assert can_transition(CaseStatus.ESCALATED, CaseStatus.RESOLVED) is True

def test_in_review_cannot_transition_to_assigned():
    assert can_transition(CaseStatus.IN_REVIEW, CaseStatus.ASSIGNED) is False

def test_unassigned_cannot_transition_to_in_review():
    assert can_transition(CaseStatus.UNASSIGNED, CaseStatus.IN_REVIEW) is False

def test_assigned_cannot_transition_to_unassigned():
    assert can_transition(CaseStatus.ASSIGNED, CaseStatus.UNASSIGNED) is False

def test_resolved_cannot_transition_to_anything():
    for status in CaseStatus:
        assert can_transition(CaseStatus.RESOLVED, status) is False
