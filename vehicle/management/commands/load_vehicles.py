import json
from django.conf import settings
from django.core.management.base import BaseCommand

from vehicle.models import Vehicle


class Command(BaseCommand):
    help = "Load vehicles from JSON file"

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / "data" / "vehicles.json"

        if not file_path.exists():
            self.stderr.write("vehicles.json not found")
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        vehicles = []
        for item in data:
            vehicles.append(
                Vehicle(
                    name=item["name"],
                    brand=item["brand"],
                    model=item["model"],
                    year=item["year"],
                    plate_number=item["plate_number"],
                    color=item["color"],
                    daily_rate=item["daily_rate"],
                    is_available=item["is_available"],
                    location=item["location"],
                )
            )

        Vehicle.objects.bulk_create(vehicles, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(f"Inserted {len(vehicles)} vehicles")
        )