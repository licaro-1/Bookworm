import uuid
from typing import Optional

from feedback.models import Feedback


class FeedbackRepository:
    """Feedback repository."""

    def get_feedback_by_uuid(self, uuid: uuid.UUID) -> Optional[Feedback]:
        return Feedback.objects.filter(uuid=uuid).first()

    def delete_feedback_by_uuid(self, feedback: Feedback) -> None:
        feedback.delete()


feedback_repository = FeedbackRepository()
