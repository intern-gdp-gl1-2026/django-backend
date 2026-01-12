from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from vehicle.domain.entities import Vehicle


class VehicleRepository(ABC):
    """Repository contract for vehicles"""

    @abstractmethod
    def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        """Fetch vehicle by id"""
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[Vehicle]:
        """List all vehicles"""
        raise NotImplementedError

    @abstractmethod
    def list_available(
        self,
        location: str,
        start_date: date,
        end_date: date,
    ) -> List[Vehicle]:
        """List available vehicles filtered by location and date range"""
        raise NotImplementedError

    @abstractmethod
    def save(self, vehicle: Vehicle) -> Vehicle:
        """Create or update vehicle"""
        raise NotImplementedError

    @abstractmethod
    def delete(self, vehicle_id: int) -> None:
        """Delete vehicle by id"""
        raise NotImplementedError
