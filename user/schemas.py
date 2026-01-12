"""
User Schemas (Simplified)
"""
from ninja import Schema
from uuid import UUID
from datetime import datetime


# ==================== REQUEST ====================

class RegisterRequest(Schema):
    username: str
    password: str


class LoginRequest(Schema):
    username: str
    password: str


# ==================== RESPONSE ====================

class UserResponse(Schema):
    id: UUID
    username: str
    created_at: datetime


class MessageResponse(Schema):
    message: str


class ErrorResponse(Schema):
    error: str
