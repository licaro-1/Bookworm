from typing import Optional

from django.contrib.auth import get_user_model

from .repository import user_repository

User = get_user_model()


class UserService:
    """User service."""
    def __init__(self):
        self.repository = user_repository

    def check_user_exists_by_username(self, username: str) -> Optional[User]:
        user = self.repository.get_user_by_username(username)
        return user


user_service = UserService()
