from dataclasses import dataclass
from typing import Optional


@dataclass
class Vehicle:
    """Represents a vehicle in the domain layer"""
    id: Optional[int]
    name: str
    brand: str
    model: str
    year: int
    plate_number: str
    color: str
    daily_rate: int
    is_available: bool
    location: str

    def mark_unavailable(self) -> None:
        """Mark vehicle as not available"""
        self.is_available = False

    def mark_available(self) -> None:
        """Mark vehicle as available"""
        self.is_available = True

    def can_be_booked(self) -> bool:
        """Check if vehicle can be booked"""
        return self.is_available
