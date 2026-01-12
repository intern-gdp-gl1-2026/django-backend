"""
Reservation Tests - Unit Tests for Reservation Domain
"""
from django.test import TestCase
from datetime import date, timedelta
from uuid import uuid4

from reservation.models import Reservation
from reservation.services import ReservationService
from reservation.schemas import AddReservationRequest, UpdateReservationRequest
from user.models import User
from vehicle.models import Vehicle


class ReservationModelTest(TestCase):
    """Tests for Reservation model."""
    
    def setUp(self):
        """Set up test data."""
        # Create test user
        self.user = User.objects.create(
            username='testuser',
            password='hashedpassword123'
        )
        
        # Create test vehicle
        self.vehicle = Vehicle.objects.create(
            name='Toyota Avanza',
            brand='Toyota',
            model='Avanza',
            year=2022,
            plate_number='B 1234 ABC',
            color='Black',
            daily_rate=350000,
            is_available=True,
            location='Jakarta'
        )
        
        # Create test reservation
        self.reservation = Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='pending'
        )
    
    def test_reservation_str(self):
        """Test reservation string representation."""
        self.assertIn(self.user.username, str(self.reservation))
    
    def test_reservation_is_active_future(self):
        """Test is_active returns True for future reservations."""
        self.assertTrue(self.reservation.is_active())
    
    def test_reservation_is_active_past(self):
        """Test is_active returns False for past reservations."""
        self.reservation.end_date = date.today() - timedelta(days=1)
        self.reservation.save()
        self.assertFalse(self.reservation.is_active())


class ReservationServiceTest(TestCase):
    """Tests for ReservationService."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create(
            username='testuser',
            password='hashedpassword123'
        )
        self.user2 = User.objects.create(
            username='testuser2',
            password='hashedpassword123'
        )
        
        self.vehicle = Vehicle.objects.create(
            name='Toyota Avanza',
            brand='Toyota',
            model='Avanza',
            year=2022,
            plate_number='B 1234 ABC',
            color='Black',
            daily_rate=350000,
            is_available=True,
            location='Jakarta'
        )
        self.vehicle2 = Vehicle.objects.create(
            name='Honda Brio',
            brand='Honda',
            model='Brio',
            year=2023,
            plate_number='B 5678 XYZ',
            color='White',
            daily_rate=280000,
            is_available=True,
            location='Bandung'
        )
    
    # ==================== GET TESTS ====================
    
    def test_get_all_empty(self):
        """Test get_all returns empty list when no reservations."""
        result = ReservationService.get_all()
        self.assertEqual(len(result), 0)
    
    def test_get_all_with_data(self):
        """Test get_all returns all reservations."""
        Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='pending'
        )
        Reservation.objects.create(
            user=self.user2,
            vehicle=self.vehicle2,
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=7),
            status='confirmed'
        )
        
        result = ReservationService.get_all()
        self.assertEqual(len(result), 2)
    
    def test_get_by_id_exists(self):
        """Test get_by_id returns reservation when exists."""
        reservation = Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='pending'
        )
        
        result = ReservationService.get_by_id(reservation.id)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, reservation.id)
    
    def test_get_by_id_not_exists(self):
        """Test get_by_id returns None when not exists."""
        result = ReservationService.get_by_id(uuid4())
        self.assertIsNone(result)
    
    # ==================== SEARCH TESTS ====================
    
    def test_search_by_user(self):
        """Test search filters by user_id."""
        Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='pending'
        )
        Reservation.objects.create(
            user=self.user2,
            vehicle=self.vehicle2,
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=7),
            status='confirmed'
        )
        
        result = ReservationService.search(user_id=self.user.id)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].user_id, self.user.id)
    
    def test_search_by_vehicle(self):
        """Test search filters by vehicle_id."""
        Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='pending'
        )
        
        result = ReservationService.search(vehicle_id=self.vehicle.id)
        self.assertEqual(len(result), 1)
    
    # ==================== AVAILABILITY TESTS ====================
    
    def test_vehicle_available_no_reservations(self):
        """Test vehicle is available when no reservations."""
        result = ReservationService.is_vehicle_available(
            self.vehicle.id,
            date.today() + timedelta(days=1),
            date.today() + timedelta(days=3)
        )
        self.assertTrue(result)
    
    def test_vehicle_not_available_overlap(self):
        """Test vehicle not available when dates overlap."""
        Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=5),
            status='confirmed'
        )
        
        result = ReservationService.is_vehicle_available(
            self.vehicle.id,
            date.today() + timedelta(days=1),
            date.today() + timedelta(days=3)
        )
        self.assertFalse(result)
    
    def test_vehicle_available_no_overlap(self):
        """Test vehicle is available when dates don't overlap."""
        Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='confirmed'
        )
        
        result = ReservationService.is_vehicle_available(
            self.vehicle.id,
            date.today() + timedelta(days=5),
            date.today() + timedelta(days=7)
        )
        self.assertTrue(result)
    
    def test_vehicle_available_cancelled_reservation(self):
        """Test vehicle is available when existing reservation is cancelled."""
        Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='cancelled'
        )
        
        result = ReservationService.is_vehicle_available(
            self.vehicle.id,
            date.today() + timedelta(days=1),
            date.today() + timedelta(days=3)
        )
        self.assertTrue(result)
    
    # ==================== CREATE TESTS ====================
    
    def test_create_success(self):
        """Test successful reservation creation."""
        payload = AddReservationRequest(
            user_id=self.user.id,
            vehicle_id=self.vehicle.id,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3)
        )
        
        result = ReservationService.create(payload)
        
        self.assertIsNotNone(result.id)
        self.assertEqual(result.user_id, self.user.id)
        self.assertEqual(result.vehicle_id, self.vehicle.id)
        self.assertEqual(result.status, 'pending')
    
    def test_create_fails_vehicle_not_available(self):
        """Test create fails when vehicle is not available."""
        Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=5),
            status='confirmed'
        )
        
        payload = AddReservationRequest(
            user_id=self.user2.id,
            vehicle_id=self.vehicle.id,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=4)
        )
        
        with self.assertRaises(ValueError) as context:
            ReservationService.create(payload)
        
        self.assertIn("not available", str(context.exception))
    
    def test_create_fails_invalid_dates(self):
        """Test create fails when start_date >= end_date."""
        payload = AddReservationRequest(
            user_id=self.user.id,
            vehicle_id=self.vehicle.id,
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=3)
        )
        
        with self.assertRaises(ValueError) as context:
            ReservationService.create(payload)
        
        self.assertIn("before end date", str(context.exception))
    
    def test_create_fails_past_date(self):
        """Test create fails when start_date is in the past."""
        payload = AddReservationRequest(
            user_id=self.user.id,
            vehicle_id=self.vehicle.id,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=3)
        )
        
        with self.assertRaises(ValueError) as context:
            ReservationService.create(payload)
        
        self.assertIn("past", str(context.exception))
    
    # ==================== DELETE TESTS ====================
    
    def test_delete_success(self):
        """Test successful deletion."""
        reservation = Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='pending'
        )
        
        result = ReservationService.delete(reservation.id)
        self.assertTrue(result)
        self.assertIsNone(ReservationService.get_by_id(reservation.id))
    
    def test_delete_not_found(self):
        """Test delete returns False when not found."""
        result = ReservationService.delete(uuid4())
        self.assertFalse(result)
    
    # ==================== CANCEL TESTS ====================
    
    def test_cancel_success(self):
        """Test successful cancellation."""
        reservation = Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='pending'
        )
        
        result = ReservationService.cancel(reservation.id)
        self.assertEqual(result.status, 'cancelled')
    
    def test_cancel_fails_completed(self):
        """Test cancel fails for completed reservation."""
        reservation = Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='completed'
        )
        
        with self.assertRaises(ValueError) as context:
            ReservationService.cancel(reservation.id)
        
        self.assertIn("completed", str(context.exception))
    
    def test_cancel_fails_already_cancelled(self):
        """Test cancel fails for already cancelled reservation."""
        reservation = Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='cancelled'
        )
        
        with self.assertRaises(ValueError) as context:
            ReservationService.cancel(reservation.id)
        
        self.assertIn("already cancelled", str(context.exception))
    
    # ==================== CONFIRM TESTS ====================
    
    def test_confirm_success(self):
        """Test successful confirmation."""
        reservation = Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='pending'
        )
        
        result = ReservationService.confirm(reservation.id)
        self.assertEqual(result.status, 'confirmed')
    
    def test_confirm_fails_not_pending(self):
        """Test confirm fails for non-pending reservation."""
        reservation = Reservation.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            status='confirmed'
        )
        
        with self.assertRaises(ValueError) as context:
            ReservationService.confirm(reservation.id)
        
        self.assertIn("Cannot confirm", str(context.exception))
