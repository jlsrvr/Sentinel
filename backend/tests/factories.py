import factory
from app.models.queue import Queue
from app.models.case import Case
from app.models.enums import ContentType, Severity, CaseStatus

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