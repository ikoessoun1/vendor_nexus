
from django.apps import AppConfig
from django.conf import settings

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError

        User = get_user_model()
        try:
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username=settings.ADMIN_USER,
                    email=settings.ADMIN_EMAIL,
                    password=settings.ADMIN_PASS,
                )
                print("✅ Superuser created")
        except OperationalError:
            # Database might not be ready yet
            pass
