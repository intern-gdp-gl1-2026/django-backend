"""
User Application Services (Simplified)
"""
from typing import Optional, List
from uuid import UUID

from user.models import User


class UserService:
    """User business operations."""
    
    @staticmethod
    def register(username: str, password: str) -> User:
        """Register a new user."""
        if User.objects.filter(username=username.lower().strip()).exists():
            raise ValueError("Username already exists")
        
        user = User.create(username=username, password=password)
        user.save()
        return user
    
    @staticmethod
    def login(username: str, password: str) -> User:
        """Authenticate user."""
        try:
            user = User.objects.get(username=username.lower().strip())
        except User.DoesNotExist:
            raise ValueError("Invalid username or password")
        
        if not user.verify_password(password):
            raise ValueError("Invalid username or password")
        
        return user
    
    @staticmethod
    def get_by_id(user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_all() -> List[User]:
        """Get all users."""
        return list(User.objects.all())
    
    @staticmethod
    def delete(user_id: UUID) -> bool:
        """Delete a user."""
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False
