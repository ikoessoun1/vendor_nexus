#users/models/unit_model.py
from django.db import models
from django.conf import settings

class Unit(models.Model):
    department = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        related_name='units'
    )
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='units_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['department', 'name'],
                name='unique_unit_per_department'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.department.name})"
