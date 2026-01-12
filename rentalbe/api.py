"""
Main API Configuration

This is where all routers from different domains are combined.
Each domain (user, vehicle, reservation) has its own router.
"""
from ninja import NinjaAPI

from user.api import router as user_router
from vehicle.api import router as vehicle_router

# Create the main API instance
api = NinjaAPI(
    title="Rental Car API",
    version="1.0.0",
    description="API for car rental management system with DDD + Clean Architecture"
)

# ==================== REGISTER ROUTERS ====================

# User domain endpoints
api.add_router("/users", user_router)

# Vehicle domain endpoints
api.add_router("/vehicles", vehicle_router)

# TODO: Add more routers as you implement them
# api.add_router("/reservations", reservation_router)


# ==================== HEALTH CHECK ====================

@api.get("/health", tags=["System"])
def health_check(request):
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}