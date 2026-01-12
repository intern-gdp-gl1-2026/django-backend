"""
Reservation Schemas - Request/Response Contracts
"""
from ninja import Schema
from datetime import date
from typing import Optional


# ========== REQUEST ==========

class AddReservationRequest(Schema):
    vehicle_id: int
    user_id: int
    start_date: date
    end_date: date


class UpdateReservationRequest(Schema):
    reservation_id: int
    vehicle_id: Optional[int] = None
    user_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class SearchReservationRequest(Schema):
    user_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class IsVehicleAvailableRequest(Schema):
    vehicle_id: int
    start_date: date
    end_date: date
    exclude_id: Optional[int] = None


# ========== RESPONSE ==========

class ReservationResponse(Schema):
    id: int
    vehicle_id: int
    user_id: int
    start_date: date
    end_date: date
    status: str


class MessageResponse(Schema):
    message: str


class ErrorResponse(Schema):
    error: str
