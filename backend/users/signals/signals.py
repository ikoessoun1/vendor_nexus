from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import Department, Unit

@receiver(post_migrate)
def create_admin(sender, **kwargs):
    User = get_user_model()

    # only run once per app
    if sender.name != "users":
        return

    admin_user = getattr(settings, "ADMIN_USER", None)
    admin_pass = getattr(settings, "ADMIN_PASSWORD", None)

    if not admin_user or not admin_pass:
        return  # skip if not set

    if not User.objects.filter(username=admin_user).exists():
        try:
            # Pick a default Department and Unit (or create them if none exist)
            department, _ = Department.objects.get_or_create(name="Default Department")
            unit, _ = Unit.objects.get_or_create(name="Default Unit", department=department)

            User.objects.create_superuser(
                username=admin_user,
                email="admin@example.com",  # or settings.ADMIN_EMAIL
                password=admin_pass,
                first_name="Admin",
                last_name="User",
                department=department,
                unit=unit,
            )
            print("✅ Superuser created.")
        except Exception as e:
            print(f"⚠ Could not create superuser: {e}")
