from datetime import date
from typing import List
from ninja import Router, Query
from ninja.errors import HttpError
from vehicle.presentation.schemas import (
    VehicleResponse,
    AvailableVehicleResponse,
    CreateVehicleRequest,
    UpdateVehicleRequest,
    MessageResponse
)
from vehicle.application.service import VehicleService
from vehicle.domain.exceptions import VehicleNotFoundError

router = Router(tags=["Vehicles"])
service = VehicleService()


# ========== GET ENDPOINTS ==========

@router.get("/search", response=List[AvailableVehicleResponse])
def search_available_vehicles(
    request,
    start_date: date = Query(..., description="Start date of reservation"),
    end_date: date = Query(..., description="End date of reservation"),
    location: str = Query(..., description="Vehicle location")
):
    """
    Get available vehicles filtered by start_date, end_date, and location
    Returns vehicles that have no conflicting reservations
    """
    try:
        return service.search_available_vehicles(start_date, end_date, location)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HttpError(500, f"Error searching vehicles: {str(e)}")


@router.get("/{vehicle_id}", response=VehicleResponse)
def get_vehicle(request, vehicle_id: int):
    """Get a specific vehicle by ID"""
    try:
        return service.get_vehicle_by_id(vehicle_id)
    except VehicleNotFoundError as e:
        raise HttpError(404, str(e))


@router.get("/", response=List[VehicleResponse])
def list_all_vehicles(request):
    """Get all vehicles"""
    return service.get_all_vehicles()


# ========== CREATE ENDPOINT ==========

@router.post("/", response=VehicleResponse)
def create_vehicle(request, payload: CreateVehicleRequest):
    """Create a new vehicle"""
    try:
        return service.create_vehicle(payload)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HttpError(500, f"Error creating vehicle: {str(e)}")


# ========== UPDATE ENDPOINT ==========

@router.put("/{vehicle_id}", response=VehicleResponse)
def update_vehicle(request, vehicle_id: int, payload: UpdateVehicleRequest):
    """Update a vehicle"""
    try:
        return service.update_vehicle(vehicle_id, payload)
    except VehicleNotFoundError as e:
        raise HttpError(404, str(e))


# ========== DELETE ENDPOINT ==========

@router.delete("/{vehicle_id}", response=MessageResponse)
def delete_vehicle(request, vehicle_id: int):
    """Delete a vehicle"""
    try:
        message = service.delete_vehicle(vehicle_id)
        return {"message": message}
    except VehicleNotFoundError as e:
        raise HttpError(404, str(e))
