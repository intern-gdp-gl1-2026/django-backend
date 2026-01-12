"""
Vehicle Service Layer - Contains all business logic
"""
from datetime import date
from typing import List, Dict, Any
from django.db.models import Q
from django.shortcuts import get_object_or_404
from vehicle.models import Vehicle
from vehicle.schemas import (
    CreateVehicleRequest,
    UpdateVehicleRequest,
)
from reservation.models import Reservation


class VehicleService:
    """Service layer for vehicle operations"""

    @staticmethod
    def get_all_vehicles() -> List[Dict[str, Any]]:
        """Get all vehicles"""
        vehicles = Vehicle.objects.all()
        return [VehicleService._vehicle_to_dict(v) for v in vehicles]

    @staticmethod
    def get_vehicle_by_id(vehicle_id: int) -> Dict[str, Any]:
        """Get a specific vehicle by ID"""
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        return VehicleService._vehicle_to_dict(vehicle)

    @staticmethod
    def search_available_vehicles(
        start_date: date,
        end_date: date,
        location: str
    ) -> List[Dict[str, Any]]:
        """
        Get available vehicles by date range and location.
        """

        location = location.strip()  

        conflicting_vehicles = Reservation.objects.filter(
            Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
        ).values_list('vehicle_id', flat=True)

        available_vehicles = Vehicle.objects.exclude(
            id__in=conflicting_vehicles
        ).filter(
            is_available=True,
            location__iexact=location 
        )

        return [VehicleService._vehicle_to_dict(v) for v in available_vehicles]

    @staticmethod
    def create_vehicle(payload: CreateVehicleRequest) -> Dict[str, Any]:
        """Create a new vehicle"""
        vehicle = Vehicle.objects.create(
            name=payload.name,
            brand=payload.brand,
            model=payload.model,
            year=payload.year,
            plate_number=payload.plate_number,
            color=payload.color,
            daily_rate=payload.daily_rate,
            is_available=True,
            location=payload.location
        )
        return VehicleService._vehicle_to_dict(vehicle)

    @staticmethod
    def update_vehicle(
        vehicle_id: int,
        payload: UpdateVehicleRequest
    ) -> Dict[str, Any]:
        """Update vehicle with provided fields"""
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        # Update only provided fields
        if payload.name is not None:
            vehicle.name = payload.name
        if payload.brand is not None:
            vehicle.brand = payload.brand
        if payload.model is not None:
            vehicle.model = payload.model
        if payload.year is not None:
            vehicle.year = payload.year
        if payload.plate_number is not None:
            vehicle.plate_number = payload.plate_number
        if payload.color is not None:
            vehicle.color = payload.color
        if payload.daily_rate is not None:
            vehicle.daily_rate = payload.daily_rate
        if payload.is_available is not None:
            vehicle.is_available = payload.is_available
        if payload.location is not None:
            vehicle.location = payload.location

        vehicle.save()
        return VehicleService._vehicle_to_dict(vehicle)

    @staticmethod
    def delete_vehicle(vehicle_id: int) -> str:
        """Delete a vehicle and return success message"""
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        vehicle_name = vehicle.name
        vehicle.delete()
        return f"Vehicle '{vehicle_name}' deleted successfully"

    @staticmethod
    def _vehicle_to_dict(vehicle: Vehicle) -> Dict[str, Any]:
        """Convert Vehicle model to dictionary"""
        return {
            "id": vehicle.id,
            "name": vehicle.name,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "year": vehicle.year,
            "plate_number": vehicle.plate_number,
            "color": vehicle.color,
            "daily_rate": vehicle.daily_rate,
            "is_available": vehicle.is_available,
            "location": vehicle.location
        }
