"""
Vehicle Service Layer - Uses domain entities and repository abstraction
"""
from datetime import date
from typing import List, Dict, Any

from vehicle.domain.entities import Vehicle as VehicleEntity
from vehicle.domain.repositories import VehicleRepository
from vehicle.domain.exceptions import VehicleNotFoundError
from vehicle.infrastructure.repositories.vehicle_repository import DjangoVehicleRepository
from vehicle.presentation.schemas import CreateVehicleRequest, UpdateVehicleRequest


class VehicleService:
    """Service layer for vehicle operations (decoupled from ORM)"""

    def __init__(self, repository: VehicleRepository = None):
        self.repository = repository or DjangoVehicleRepository()

    def get_all_vehicles(self) -> List[Dict[str, Any]]:
        """Get all vehicles"""
        vehicles = self.repository.list_all()
        return [self._entity_to_dict(v) for v in vehicles]

    def get_vehicle_by_id(self, vehicle_id: int) -> Dict[str, Any]:
        """Get a specific vehicle by ID"""
        vehicle = self.repository.get_by_id(vehicle_id)
        if not vehicle:
            raise VehicleNotFoundError(f"Vehicle with id {vehicle_id} not found")
        return self._entity_to_dict(vehicle)

    def search_available_vehicles(
        self,
        start_date: date,
        end_date: date,
        location: str,
    ) -> List[Dict[str, Any]]:
        """Get available vehicles by date range and location"""
        vehicles = self.repository.list_available(location, start_date, end_date)
        return [self._entity_to_dict(v) for v in vehicles]

    def create_vehicle(self, payload: CreateVehicleRequest) -> Dict[str, Any]:
        """Create a new vehicle"""
        try:
            entity = VehicleEntity(
                id=None,
                name=payload.name,
                brand=payload.brand,
                model=payload.model,
                year=payload.year,
                plate_number=payload.plate_number,
                color=payload.color,
                daily_rate=payload.daily_rate,
                is_available=True,
                location=payload.location,
            )
            saved = self.repository.save(entity)
            return self._entity_to_dict(saved)
        except Exception as e:
            print(f"Error in service.create_vehicle: {e}")
            import traceback
            traceback.print_exc()
            raise

    def update_vehicle(
        self,
        vehicle_id: int,
        payload: UpdateVehicleRequest,
    ) -> Dict[str, Any]:
        """Update vehicle with provided fields"""
        vehicle = self.repository.get_by_id(vehicle_id)
        if not vehicle:
            raise VehicleNotFoundError(f"Vehicle with id {vehicle_id} not found")

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

        updated = self.repository.save(vehicle)
        return self._entity_to_dict(updated)

    def delete_vehicle(self, vehicle_id: int) -> str:
        """Delete a vehicle and return success message"""
        vehicle = self.repository.get_by_id(vehicle_id)
        if not vehicle:
            raise VehicleNotFoundError(f"Vehicle with id {vehicle_id} not found")
        
        vehicle_name = vehicle.name
        self.repository.delete(vehicle_id)
        return f"Vehicle '{vehicle_name}' deleted successfully"

    @staticmethod
    def _entity_to_dict(vehicle: VehicleEntity) -> Dict[str, Any]:
        """Convert Vehicle entity to dictionary"""
        return {
            "id": int(vehicle.id) if vehicle.id else None,
            "name": str(vehicle.name),
            "brand": str(vehicle.brand),
            "model": str(vehicle.model),
            "year": int(vehicle.year),
            "plate_number": str(vehicle.plate_number),
            "color": str(vehicle.color),
            "daily_rate": int(vehicle.daily_rate),
            "is_available": bool(vehicle.is_available),
            "location": str(vehicle.location)
        }
