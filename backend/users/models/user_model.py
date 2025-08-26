# users/models/user_model.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from users.utils import generate_username
from users.models.department_model import Department
from users.models.unit_model import Unit


class UserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        # Normalize
        email = self.normalize_email(email).lower()
        first_name = extra_fields.get("first_name", "").strip()
        last_name = extra_fields.get("last_name", "").strip()

        if not first_name or not last_name:
            raise ValueError("Users must have a first name and last name")

        # Auto-generate username if not provided
        if not username:
            username = generate_username(first_name, last_name)

        user = self.model(username=username.lower(), email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username=username, email=email, password=password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=101, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='users_in_unit')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email", "department", "unit"]


    objects = UserManager()

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        self.username = generate_username(self.first_name, self.last_name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.username
