"""
Main API Configuration
"""
from ninja import NinjaAPI

from user.api import router as user_router
from vehicle.presentation.api import router as vehicle_router
from reservation.api import router as reservation_router

# Create the main API instance
api = NinjaAPI(
    title="Rental Car API",
    version="1.0.0",
    description="API for car rental management system with DDD + Clean Architecture"
)

# ==================== REGISTER ROUTERS ====================

api.add_router("/users", user_router)
api.add_router("/vehicles", vehicle_router)
api.add_router("/reservations", reservation_router)


# ==================== HEALTH CHECK ====================

@api.get("/health", tags=["System"])
def health_check(request):
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}