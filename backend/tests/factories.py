import factory
from app.models.queue import Queue
from app.models.case import Case
from app.models.user import User
from app.models.decision import Decision
from app.models.enums import ContentType, Severity, CaseStatus, Role, Action, ConfidenceLevel

class QueueFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Queue
        sqlalchemy_session_persistence = "flush"

    name = factory.Sequence(lambda n: f"queue-{n}")
    required_skills = []
    severity_levels = ["low", "medium", "high", "critical"]
    sla_hours = 24

class CaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Case
        sqlalchemy_session_persistence = "flush"
        exclude = ("queue",)

    external_id = factory.Faker('uuid4')
    content_type = ContentType.TEXT
    content_ref = ""
    severity = factory.Iterator(Severity)
    status = CaseStatus.UNASSIGNED
    queue = factory.SubFactory(QueueFactory)
    queue_id = factory.LazyAttribute(lambda obj: obj.queue.id)
    source = "user_report"
    case_metadata = []


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "flush"

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    hashed_password = 'hashed+password'
    full_name = 'Test User'
    role = Role.ANALYST
    skills = []

class DecisionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Decision
        sqlalchemy_session_persistence = "flush"
        exclude = ("case", "reviewer")

    case = factory.SubFactory(CaseFactory)
    case_id = factory.LazyAttribute(lambda obj: obj.case.id)
    reviewer = factory.SubFactory(UserFactory)
    reviewer_id = factory.LazyAttribute(lambda obj: obj.reviewer.id)
    action = Action.WARN
    rationale = 'Its seems legitimate but better warn them'
    confidence = ConfidenceLevel.MEDIUM
    time_on_case_secs = 360