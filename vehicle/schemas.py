from ninja import Schema
from typing import Optional


# ========== REQUEST SCHEMAS (Input DTOs) ==========

class CreateVehicleRequest(Schema):
    """DTO for creating a new vehicle"""
    name: str
    brand: str
    model: str
    year: int
    plate_number: str
    color: str
    daily_rate: int
    location: str


class UpdateVehicleRequest(Schema):
    """DTO for updating vehicle (all fields optional)"""
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    plate_number: Optional[str] = None
    color: Optional[str] = None
    daily_rate: Optional[int] = None
    is_available: Optional[bool] = None
    location: Optional[str] = None


# ========== RESPONSE SCHEMAS (Output DTOs) ==========

class VehicleResponse(Schema):
    """DTO for vehicle response"""
    id: int
    name: str
    brand: str
    model: str
    year: int
    plate_number: str
    color: str
    daily_rate: int
    is_available: bool
    location: str


class AvailableVehicleResponse(Schema):
    """DTO for available vehicles (with availability info)"""
    id: int
    name: str
    brand: str
    model: str
    year: int
    plate_number: str
    color: str
    daily_rate: int
    is_available: bool
    location: str


# ========== ERROR SCHEMAS ==========

class MessageResponse(Schema):
    """Generic message response"""
    message: str


class ErrorResponse(Schema):
    """Error response with optional details"""
    error: str
    detail: Optional[str] = None