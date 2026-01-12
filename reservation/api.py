"""
Reservation API - HTTP Endpoints
"""
from ninja import Router
from uuid import UUID
from typing import List

from reservation.services import ReservationService
from reservation.schemas import (
    AddReservationRequest,
    UpdateReservationRequest,
    SearchReservationRequest,
    IsVehicleAvailableRequest,
    ReservationResponse,
    MessageResponse,
    ErrorResponse,
)

router = Router(tags=["Reservations"])


# ==================== ENDPOINTS ====================

@router.get("/", response=List[ReservationResponse])
def list_reservations(request):
    """Get all reservations."""
    return ReservationService.get_all()


@router.post("/search", response=List[ReservationResponse])
def search_reservations(request, payload: SearchReservationRequest):
    """Search reservations with optional filters."""
    return ReservationService.search(payload)


@router.post("/check-availability", response={200: dict, 400: ErrorResponse})
def check_vehicle_availability(request, payload: IsVehicleAvailableRequest):
    """Check if vehicle is available for the given dates."""
    is_available = ReservationService.is_vehicle_available(payload)
    return 200, {"available": is_available}


@router.get("/{reservation_id}", response={200: ReservationResponse, 404: ErrorResponse})
def get_reservation(request, reservation_id: int):
    """Get reservation by ID."""
    reservation = ReservationService.get_by_id(reservation_id)
    if not reservation:
        return 404, {"error": "Reservation not found"}
    return 200, reservation


@router.post("/", response={201: ReservationResponse, 400: ErrorResponse})
def create_reservation(request, payload: AddReservationRequest):
    """Create a new reservation."""
    try:
        print("Oi New Reservation")
        reservation = ReservationService.create(payload)
        print("RESERVATION", reservation)
        return 201, reservation
    except ValueError as e:
        return 400, {"error": str(e)}


@router.put("/", response={200: ReservationResponse, 400: ErrorResponse, 404: ErrorResponse})
def update_reservation(request, payload: UpdateReservationRequest):
    """Update a reservation."""
    try:
        reservation = ReservationService.update(payload)
        return 200, reservation
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            return 404, {"error": error_msg}
        return 400, {"error": error_msg}


@router.delete("/{reservation_id}", response={200: MessageResponse, 404: ErrorResponse})
def delete_reservation(request, reservation_id: UUID):
    """Delete a reservation."""
    if ReservationService.delete(reservation_id):
        return 200, {"message": "Reservation deleted"}
    return 404, {"error": "Reservation not found"}


@router.post("/{reservation_id}/cancel", response={200: ReservationResponse, 400: ErrorResponse, 404: ErrorResponse})
def cancel_reservation(request, reservation_id: UUID):
    """Cancel a reservation."""
    try:
        reservation = ReservationService.cancel(reservation_id)
        return 200, reservation
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            return 404, {"error": error_msg}
        return 400, {"error": error_msg}


@router.post("/{reservation_id}/confirm", response={200: ReservationResponse, 400: ErrorResponse, 404: ErrorResponse})
def confirm_reservation(request, reservation_id: UUID):
    """Confirm a reservation."""
    try:
        reservation = ReservationService.confirm(reservation_id)
        return 200, reservation
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            return 404, {"error": error_msg}
        return 400, {"error": error_msg}