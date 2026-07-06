from datetime import datetime, timedelta

from app.core.database import SessionLocal
from app.models.audit_log import AuditLog  # noqa: F401
from app.models.case import Case  # noqa: F401
from app.models.content_exposure import ContentExposure  # noqa: F401
from app.models.decision import Decision  # noqa: F401
from app.models.escalation import Escalation  # noqa: F401
from app.models.queue import Queue  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.enums import CaseStatus, Severity
from tests.factories import CaseFactory, QueueFactory


def seed():
    db = SessionLocal()
    QueueFactory._meta.sqlalchemy_session = db
    CaseFactory._meta.sqlalchemy_session = db

    try:
        general = QueueFactory.create(
            name="General Review",
            severity_levels=["low", "medium", "high", "critical"],
            sla_hours=24,
        )
        csam = QueueFactory.create(
            name="CSAM Escalations",
            required_skills=["csam_trained"],
            severity_levels=["high", "critical"],
            sla_hours=4,
        )

        now = datetime.now()

        # Critical — overdue
        CaseFactory.create(
            severity=Severity.CRITICAL,
            status=CaseStatus.UNASSIGNED,
            source="user_report",
            sla_deadline=now - timedelta(hours=1),
            queue_id=csam.id,
        )

        # Critical — 1h left
        CaseFactory.create(
            severity=Severity.CRITICAL,
            status=CaseStatus.ASSIGNED,
            source="proactive_detection",
            sla_deadline=now + timedelta(hours=1),
            queue_id=csam.id,
        )

        # High — 2h left
        CaseFactory.create(
            severity=Severity.HIGH,
            status=CaseStatus.UNASSIGNED,
            source="user_report",
            sla_deadline=now + timedelta(hours=2),
            queue_id=general.id,
        )

        # High — 6h left
        CaseFactory.create(
            severity=Severity.HIGH,
            status=CaseStatus.IN_REVIEW,
            source="automated_classifier",
            sla_deadline=now + timedelta(hours=6),
            queue_id=general.id,
        )

        # High — 8h left
        CaseFactory.create(
            severity=Severity.HIGH,
            status=CaseStatus.UNASSIGNED,
            source="user_report",
            sla_deadline=now + timedelta(hours=8),
            queue_id=general.id,
        )

        # Medium — 12h left
        CaseFactory.create(
            severity=Severity.MEDIUM,
            status=CaseStatus.UNASSIGNED,
            source="user_report",
            sla_deadline=now + timedelta(hours=12),
            queue_id=general.id,
        )

        # Medium — 18h left
        CaseFactory.create(
            severity=Severity.MEDIUM,
            status=CaseStatus.ASSIGNED,
            source="proactive_detection",
            sla_deadline=now + timedelta(hours=18),
            queue_id=general.id,
        )

        # Medium — 20h left
        CaseFactory.create(
            severity=Severity.MEDIUM,
            status=CaseStatus.UNASSIGNED,
            source="automated_classifier",
            sla_deadline=now + timedelta(hours=20),
            queue_id=general.id,
        )

        # Low — 24h left
        CaseFactory.create(
            severity=Severity.LOW,
            status=CaseStatus.UNASSIGNED,
            source="user_report",
            sla_deadline=now + timedelta(hours=24),
            queue_id=general.id,
        )

        # Low — no deadline
        CaseFactory.create(
            severity=Severity.LOW,
            status=CaseStatus.UNASSIGNED,
            source="user_report",
            sla_deadline=None,
            queue_id=general.id,
        )

        db.commit()
        print("✓ Seeded 2 queues and 10 cases")

    except Exception as e:
        db.rollback()
        print(f"✗ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()