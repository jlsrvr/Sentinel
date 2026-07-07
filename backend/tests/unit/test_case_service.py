import uuid
import pytest
from freezegun import freeze_time
from datetime import datetime
from tests.factories import CaseFactory
from app.models.enums import CaseStatus
from app.services.case import can_transition, transition, assign, start_review
from app.core.exceptions import InvalidTransitionError

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

def test_transition_updates_the_case_status():
    case = CaseFactory.build(status=CaseStatus.UNASSIGNED)
    target_status = CaseStatus.ASSIGNED

    transition(case, target_status)

    assert case.status == target_status

def test_transition_raises_exception_when_transition_invalid():
    starting_status = CaseStatus.ASSIGNED
    case = CaseFactory.build(status = starting_status)
    target_status = CaseStatus.UNASSIGNED

    with pytest.raises(InvalidTransitionError) as e_info:
        transition(case, target_status)
    assert starting_status.value in str(e_info.value).lower()
    assert target_status.value in str(e_info.value).lower()

@freeze_time("2024-01-15 10:00:00")
def test_transition_to_assigned_sets_assigned_at():
    case = CaseFactory.build(status=CaseStatus.UNASSIGNED)

    transition(case, CaseStatus.ASSIGNED)

    assert case.assigned_at == datetime(2024, 1, 15, 10, 0, 0)
    assert case.resolved_at == None

@freeze_time("2024-01-15 10:00:00")
def test_transition_to_resolved_sets_resolved_at():
    assigned_at = datetime(2024, 1, 9, 10, 0, 0)
    case = CaseFactory.build(status=CaseStatus.IN_REVIEW, assigned_at=assigned_at)

    transition(case, CaseStatus.RESOLVED)

    assert case.assigned_at == assigned_at
    assert case.resolved_at == datetime(2024, 1, 15, 10, 0, 0)

@freeze_time("2024-01-15 10:00:00")
def test_assign_sets_reviewer_id():
    case = CaseFactory.build(status=CaseStatus.UNASSIGNED)
    reviewer_id = uuid.uuid4

    assign(case, reviewer_id)

    assert case.assigned_at == datetime(2024, 1, 15, 10, 0, 0)
    assert case.assigned_to == reviewer_id

def test_start_review_changes_status_to_in_review():
    case = CaseFactory.build(status=CaseStatus.ASSIGNED)

    start_review(case)

    assert case.status == CaseStatus.IN_REVIEW