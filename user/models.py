"""
User Model - Simple DDD + Clean Architecture
"""
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    """
    User Entity - simple models.Model
    Fields: id (auto), username, password
    """
    
    # id otomatis dibuat Django sebagai AutoField (integer)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.username
    
    # ========== DOMAIN LOGIC ==========
    
    def set_password(self, raw_password: str) -> None:
        """Hash and set password."""
        if len(raw_password) < 6:
            raise ValueError("Password must be at least 6 characters")
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password: str) -> bool:
        """Check if password matches."""
        return check_password(raw_password, self.password)
    
    @classmethod
    def create(cls, username: str, password: str) -> 'User':
        """Factory method to create user with validation."""
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        user = cls(username=username.strip().lower())
        user.set_password(password)
        return user
