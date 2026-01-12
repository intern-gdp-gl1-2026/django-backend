<<<<<<< HEAD
from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
=======
"""
User Domain Model (Simplified)
"""
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from uuid import uuid4


class User(models.Model):
    """
    User Entity - Simple version with id, username, password
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.username
    
    # ==================== DOMAIN LOGIC ====================
    
    def set_password(self, raw_password: str) -> None:
        """Hash and set password."""
        if len(raw_password) < 6:
            raise ValueError("Password must be at least 6 characters")
        self.password_hash = make_password(raw_password)
    
    def verify_password(self, raw_password: str) -> bool:
        """Check if password matches."""
        return check_password(raw_password, self.password_hash)
    
    # ==================== FACTORY METHOD ====================
    
    @classmethod
    def create(cls, username: str, password: str) -> 'User':
        """Create a new user with validation."""
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        
        user = cls(username=username.strip().lower())
        user.set_password(password)
        return user
>>>>>>> ad47ace (fix: user schema)
