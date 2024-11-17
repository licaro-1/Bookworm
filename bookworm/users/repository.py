from typing import Optional

from users.models import User


class UserRepository:
    """User repository."""

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return User.objects.filter(username=username).first()

    def get_user_by_id(self, uid: int) -> Optional[User]:
        """Get user by id."""
        return User.objects.filter(id=uid).first()

    def create_user(self, username: str, email: str, password: str) -> User:
        """Create user and return obj."""
        return User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

    def update_user(self, user: User, **kwargs) -> User:
        """Partial update user."""
        for key, val in kwargs.items():
            setattr(user, key, val)
        user.save()
        return user

    def delete_user(self, user: User) -> None:
        """Delete user."""
        return user.delete()


user_repository = UserRepository()
