import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from user.models import User
from reservation.models import Reservation
from vehicle.models import Vehicle


class Command(BaseCommand):
    help = "Load reservations from JSON file"

    def handle(self, *args, **options):
        data_file = Path(settings.BASE_DIR) / "data" / "reservations.json"

        if not data_file.exists():
            self.stderr.write(self.style.ERROR("reservations.json not found"))
            return

        with open(data_file, "r") as f:
            reservations = json.load(f)

        created_count = 0
        skipped_count = 0

        for item in reservations:
            try:
                user = User.objects.get(id=item["user"])
                vehicle = Vehicle.objects.get(id=item["vehicle"])

                if Reservation.objects.filter(
                    user=user,
                    vehicle=vehicle,
                    start_date=item["start_date"],
                    end_date=item["end_date"]
                ).exists():
                    self.stdout.write(
                        self.style.WARNING(
                            f"Reservation for user {user.username} and vehicle {vehicle.name} "
                            f"on {item['start_date']} already exists, skipped"
                        )
                    )
                    skipped_count += 1
                    continue

                reservation = Reservation.objects.create(
                    user=user,
                    vehicle=vehicle,
                    start_date=item["start_date"],
                    end_date=item["end_date"],
                    status=item["status"],
                )
                created_count += 1

            except User.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f"User with id {item['user']} not found")
                )
                skipped_count += 1
            except Vehicle.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f"Vehicle with id {item['vehicle']} not found")
                )
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {created_count} reservations (skipped: {skipped_count})"
            )
        )
