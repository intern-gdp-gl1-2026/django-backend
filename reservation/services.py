"""
Reservation Service - Business Logic Layer
"""
from typing import List, Optional
from uuid import UUID
from datetime import date

from reservation.models import Reservation
from reservation.schemas import (
    AddReservationRequest,
    UpdateReservationRequest,
    SearchReservationRequest,
    IsVehicleAvailableRequest
)


class ReservationService:
    """Handles all reservation business operations."""
    
    @staticmethod
    def get_all() -> List[ReservationResponse]:
        """Get all reservations."""
        try:
            return list(Reservation.objects.all())
        except Exception as e:
            print(e.__str__())
            return []
    
    @staticmethod
    def get_by_id(reservation_id: int) -> Optional[Reservation]:
        """Get reservation by ID."""
        try:
            return Reservation.objects.get(id=reservation_id)
        except:
            return None
    
    @staticmethod
    def search(
       payload: SearchReservationRequest
    ) -> List[Reservation]:
        """Search reservations with optional filters."""
        queryset = Reservation.objects.all()
        
        if payload.user_id:
            queryset = queryset.filter(user_id=payload.user_id)
        if payload.vehicle_id:
            queryset = queryset.filter(vehicle_id=payload.vehicle_id)
        if payload.start_date:
            queryset = queryset.filter(start_date__gte=payload.start_date)
        if payload.end_date:
            queryset = queryset.filter(end_date__lte=payload.end_date)
        
        return list(queryset)
    
    @staticmethod
    def is_vehicle_available(payload: IsVehicleAvailableRequest) -> bool:
        """Check if vehicle is available for the given dates."""
        queryset = Reservation.objects.filter(
            vehicle_id=payload.vehicle_id,
            start_date__lte=payload.end_date,
            end_date__gte=payload.start_date,
            status__in=['pending', 'confirmed']
        )
        
        if payload.exclude_id:
            queryset = queryset.exclude(id=payload.exclude_id)
        
        return not queryset.exists()
    
    @staticmethod
    def create(payload: AddReservationRequest) -> Reservation:
        """Create a new reservation."""
        print("Creating reservation...")
        # Validate dates
        if payload.start_date >= payload.end_date:
            raise ValueError("Start date must be before end date")
        
        if payload.start_date < date.today():
            raise ValueError("Start date cannot be in the past")
        
        try:
            # Check availability
            availability_check = IsVehicleAvailableRequest(
                vehicle_id=payload.vehicle_id,
                start_date=payload.start_date,
                end_date=payload.end_date
        )
        except Exception as e:
            raise ValueError("Vehicle is not available for the selected dates")
        
        if not ReservationService.is_vehicle_available(availability_check):
            raise ValueError("Vehicle is not available for the selected dates")
        
        # Create reservation
        print("Creating reservation...")
        reservation = Reservation.objects.create(
            user_id=payload.user_id,
            vehicle_id=payload.vehicle_id,
            start_date=payload.start_date,
            end_date=payload.end_date,
            status='pending'
        )
        print("Reservation created successfully")
        return reservation
    
    @staticmethod
    def update(payload: UpdateReservationRequest) -> Reservation:
        """Update a reservation."""
        reservation = ReservationService.get_by_id(payload.reservation_id)
        if not reservation:
            raise ValueError("Reservation not found")
        
        # Check if can be updated (not completed or cancelled)
        if reservation.status in ['completed', 'cancelled']:
            raise ValueError(f"Cannot update {reservation.status} reservation")
        
        # Validate dates if being changed
        new_start = payload.start_date or reservation.start_date
        new_end = payload.end_date or reservation.end_date
        new_vehicle = payload.vehicle_id or reservation.vehicle_id
        
        if new_start >= new_end:
            raise ValueError("Start date must be before end date")
        
        # Check availability (excluding current reservation)
        availability_check = IsVehicleAvailableRequest(
            vehicle_id=new_vehicle,
            start_date=new_start,
            end_date=new_end,
            exclude_id=payload.reservation_id
        )
        if not ReservationService.is_vehicle_available(availability_check):
            raise ValueError("Vehicle is not available for the selected dates")
        
        # Update fields
        if payload.vehicle_id:
            reservation.vehicle_id = payload.vehicle_id
        if payload.user_id:
            reservation.user_id = payload.user_id
        if payload.start_date:
            reservation.start_date = payload.start_date
        if payload.end_date:
            reservation.end_date = payload.end_date
        
        reservation.save()
        return reservation
    
    @staticmethod
    def delete(reservation_id: UUID) -> bool:
        """Delete a reservation."""
        reservation = ReservationService.get_by_id(reservation_id)
        if not reservation:
            return False
        
        reservation.delete()
        return True
    
    @staticmethod
    def cancel(reservation_id: UUID) -> Reservation:
        """Cancel a reservation."""
        reservation = ReservationService.get_by_id(reservation_id)
        if not reservation:
            raise ValueError("Reservation not found")
        
        if reservation.status == 'completed':
            raise ValueError("Cannot cancel completed reservation")
        
        if reservation.status == 'cancelled':
            raise ValueError("Reservation is already cancelled")
        
        reservation.status = 'cancelled'
        reservation.save()
        return reservation
    
    @staticmethod
    def confirm(reservation_id: UUID) -> Reservation:
        """Confirm a reservation."""
        reservation = ReservationService.get_by_id(reservation_id)
        if not reservation:
            raise ValueError("Reservation not found")
        
        if reservation.status != 'pending':
            raise ValueError(f"Cannot confirm {reservation.status} reservation")
        
        reservation.status = 'confirmed'
        reservation.save()
        return reservation
