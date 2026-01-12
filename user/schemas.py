"""
User Schemas - Request/Response Contracts
"""
from ninja import Schema


# ========== REQUEST ==========

class RegisterRequest(Schema):
    username: str
    password: str


class LoginRequest(Schema):
    username: str
    password: str


# ========== RESPONSE ==========

class UserResponse(Schema):
    id: int
    username: str


class MessageResponse(Schema):
    message: str


class ErrorResponse(Schema):
    error: str
