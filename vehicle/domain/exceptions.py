"""
Domain-specific exceptions for vehicle
"""


class VehicleNotFoundError(Exception):
    """Raised when a vehicle is not found"""


class VehicleUnavailableError(Exception):
    """Raised when a vehicle is not available to be booked"""


class DuplicatePlateNumberError(Exception):
    """Raised when plate number uniqueness is violated"""
