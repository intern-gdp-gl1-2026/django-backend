from datetime import date
from typing import List, Optional
from django.db.models import Q

from vehicle.domain.entities import Vehicle as VehicleEntity
from vehicle.domain.repositories import VehicleRepository
from vehicle.domain.exceptions import VehicleNotFoundError
from vehicle.models import Vehicle as VehicleModel
from reservation.models import Reservation


class DjangoVehicleRepository(VehicleRepository):
    """Vehicle repository backed by Django ORM"""

    def get_by_id(self, vehicle_id: int) -> Optional[VehicleEntity]:
        """Fetch vehicle by id"""
        vehicle = VehicleModel.objects.filter(id=vehicle_id).first()
        if not vehicle:
            return None
        return self._to_entity(vehicle)

    def list_all(self) -> List[VehicleEntity]:
        """List all vehicles"""
        vehicles = VehicleModel.objects.all()
        return [self._to_entity(v) for v in vehicles]

    def list_available(
        self,
        location: str,
        start_date: date,
        end_date: date,
    ) -> List[VehicleEntity]:
        """List available vehicles filtered by location and date range"""
        # Find vehicles that have overlapping reservations
        conflicting_ids = Reservation.objects.filter(
            Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
        ).values_list("vehicle_id", flat=True)

        vehicles = (
            VehicleModel.objects.exclude(id__in=conflicting_ids)
            .filter(is_available=True, location__iexact=location.strip())
        )
        return [self._to_entity(v) for v in vehicles]

    def save(self, vehicle: VehicleEntity) -> VehicleEntity:
        """Create or update vehicle"""
        if vehicle.id:
            db_vehicle = VehicleModel.objects.get(id=vehicle.id)
        else:
            db_vehicle = VehicleModel()

        db_vehicle.name = vehicle.name
        db_vehicle.brand = vehicle.brand
        db_vehicle.model = vehicle.model
        db_vehicle.year = vehicle.year
        db_vehicle.plate_number = vehicle.plate_number
        db_vehicle.color = vehicle.color
        db_vehicle.daily_rate = vehicle.daily_rate
        db_vehicle.is_available = vehicle.is_available
        db_vehicle.location = vehicle.location
        db_vehicle.save()

        return self._to_entity(db_vehicle)

    def delete(self, vehicle_id: int) -> None:
        """Delete vehicle by id"""
        deleted, _ = VehicleModel.objects.filter(id=vehicle_id).delete()
        if not deleted:
            raise VehicleNotFoundError(f"Vehicle with id {vehicle_id} not found")

    @staticmethod
    def _to_entity(model: VehicleModel) -> VehicleEntity:
        """Map Django ORM model to domain entity"""
        return VehicleEntity(
            id=model.id,
            name=model.name,
            brand=model.brand,
            model=model.model,
            year=model.year,
            plate_number=model.plate_number,
            color=model.color,
            daily_rate=model.daily_rate,
            is_available=model.is_available,
            location=model.location,
        )
