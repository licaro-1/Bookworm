import uuid

from feedback.repository import feedback_repository
from logger.log import logger


class FeedbackService:
    """Feedback service."""
    def __init__(self):
        self.repository = feedback_repository

    def get_feedback_by_uuid(self, uuid: uuid.UUID):
        logger.info(
            f"Starting getting Feedback by {uuid=}"
        )
        feedback = self.repository.get_feedback_by_uuid(uuid)
        logger.info(f"Get Feedback {uuid}: {feedback}")
        return feedback


feedback_service = FeedbackService()
