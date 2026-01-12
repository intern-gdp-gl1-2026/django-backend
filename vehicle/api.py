from datetime import date
from typing import List
from ninja import Router, Query
from vehicle.schemas import (
    VehicleResponse,
    AvailableVehicleResponse,
    CreateVehicleRequest,
    UpdateVehicleRequest,
    MessageResponse
)
from vehicle.service import VehicleService

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
    return service.search_available_vehicles(start_date, end_date, location)


@router.get("/", response=List[VehicleResponse])
def list_all_vehicles(request):
    """Get all vehicles"""
    return service.get_all_vehicles()


@router.get("/{vehicle_id}", response=VehicleResponse)
def get_vehicle(request, vehicle_id: int):
    """Get a specific vehicle by ID"""
    return service.get_vehicle_by_id(vehicle_id)


# ========== CREATE ENDPOINT ==========

@router.post("/", response=VehicleResponse)
def create_vehicle(request, payload: CreateVehicleRequest):
    """Create a new vehicle"""
    return service.create_vehicle(payload)


# ========== UPDATE ENDPOINT ==========

@router.put("/{vehicle_id}", response=VehicleResponse)
def update_vehicle(request, vehicle_id: int, payload: UpdateVehicleRequest):
    """Update a vehicle"""
    return service.update_vehicle(vehicle_id, payload)


# ========== DELETE ENDPOINT ==========

@router.delete("/{vehicle_id}", response=MessageResponse)
def delete_vehicle(request, vehicle_id: int):
    """Delete a vehicle"""
    message = service.delete_vehicle(vehicle_id)
    return {"message": message}
