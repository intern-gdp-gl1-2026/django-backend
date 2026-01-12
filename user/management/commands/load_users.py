import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from user.models import User


class Command(BaseCommand):
    help = "Load users from JSON file"

    def handle(self, *args, **options):
        data_file = Path(settings.BASE_DIR) / "data" / "users.json"

        if not data_file.exists():
            self.stderr.write(self.style.ERROR("users.json not found"))
            return

        with open(data_file, "r") as f:
            users = json.load(f)

        created_count = 0

        for item in users:
            username = item["username"]
            password = item["password"]

            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f"User '{username}' already exists, skipped")
                )
                continue

            # Use our User.create factory method
            user = User.create(username=username, password=password)
            user.save()
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} users")
        )
