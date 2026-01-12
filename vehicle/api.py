from datetime import date
from ninja import NinjaAPI, Query
from sympy import Q
from vehicle.models import Vehicle
from vehicle.schema import VehicleSchema
from reservation.models import Reservation
from typing import List


api = NinjaAPI()

@api.get("/vehicles", response=List[VehicleSchema])
def list_vehicles(request, start_date:date = Query(...), end_date:date = Query(...), location:str=Query(...)):
   
    unavailable_vehicles = Reservation.objects.filter(
        Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
    ).values_list('vehicle_id', flat=True)

    available_vehicles = Vehicle.objects.exclude(id__in=unavailable_vehicles).filter(
    is_active=True,
    location=location
)

    return available_vehicles