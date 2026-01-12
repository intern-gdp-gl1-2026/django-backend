from ninja import Schema

class VehicleBase(Schema):
    name: str
    brand: str
    model: str
    year: int
    plate_number: str
    color: str
    daily_rate: int
    is_available: bool
    location: str

class NotFoundSchema(Schema):
    message: str