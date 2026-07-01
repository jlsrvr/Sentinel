import uuid
from sqlalchemy import select
from app.models.enums import Action, ConfidenceLevel, CaseStatus
from app.models.decision import Decision

VALID_DECISION_BODY = {
    "action": Action.ESCALATE.value,
    "rationale": "bad things happened",
    "policy_reference": None,
    "confidence": ConfidenceLevel.HIGH.value,
    "time_on_case_secs": 600,
}

def test_decision_create_returns_201_when_valid(authenticated_client, case_factory):
    case = case_factory.create(status=CaseStatus.IN_REVIEW)

    response = authenticated_client.post(f"/api/v1/cases/{case.id}/decisions", json=VALID_DECISION_BODY)

    assert response.status_code == 201

def test_decision_create_persists_decision(authenticated_client, case_factory, db):
    case = case_factory.create(status=CaseStatus.IN_REVIEW)

    decisions = db.execute(select(Decision)).scalars().all()
    assert len(decisions) == 0

    authenticated_client.post(f"/api/v1/cases/{case.id}/decisions", json=VALID_DECISION_BODY)

    decisions = db.execute(select(Decision)).scalars().all()
    assert len(decisions) == 1

def test_decision_create_returns_404_when_case_non_existant(authenticated_client):
    case_id = str(uuid.uuid4())

    response = authenticated_client.post(f"/api/v1/cases/{case_id}/decisions", json=VALID_DECISION_BODY)

    assert response.status_code == 404

def test_decision_create_returns_422_when_body_is_invalid(authenticated_client, case_factory):
    case = case_factory.create(status=CaseStatus.IN_REVIEW)
    invalid_body = {}

    response = authenticated_client.post(f"/api/v1/cases/{case.id}/decisions", json=invalid_body)

    assert response.status_code == 422

def test_decision_create_returns_409_when_case_not_in_review(authenticated_client, case_factory):
    case = case_factory.create(status=CaseStatus.ASSIGNED)

    response = authenticated_client.post(f"/api/v1/cases/{case.id}/decisions", json=VALID_DECISION_BODY)

    assert response.status_code == 409