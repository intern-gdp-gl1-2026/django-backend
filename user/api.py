"""
User API - HTTP Endpoints
"""
from ninja import Router
from uuid import UUID
from typing import List

from user.services import UserService
from user.schemas import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    MessageResponse,
    ErrorResponse,
)

router = Router(tags=["Users"])


@router.post("/register", response={201: UserResponse, 400: ErrorResponse})
def register(request, payload: RegisterRequest):
    """Register a new user."""
    try:
        user = UserService.register(payload.username, payload.password)
        return 201, user
    except ValueError as e:
        return 400, {"error": str(e)}


@router.post("/login", response={200: UserResponse, 401: ErrorResponse})
def login(request, payload: LoginRequest):
    """Login user."""
    try:
        user = UserService.login(payload.username, payload.password)
        return 200, user
    except ValueError as e:
        return 401, {"error": str(e)}


@router.get("/", response=List[UserResponse])
def list_users(request):
    """Get all users."""
    return UserService.get_all()


@router.get("/{user_id}", response={200: UserResponse, 404: ErrorResponse})
def get_user(request, user_id: UUID):
    """Get user by ID."""
    user = UserService.get_by_id(user_id)
    if not user:
        return 404, {"error": "User not found"}
    return 200, user


@router.delete("/{user_id}", response={200: MessageResponse, 404: ErrorResponse})
def delete_user(request, user_id: UUID):
    """Delete a user."""
    if UserService.delete(user_id):
        return 200, {"message": "User deleted"}
    return 404, {"error": "User not found"}
