from django.db import models
import uuid
from django.utils.text import slugify
from django.conf import settings

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    emails = models.TextField(help_text="Comma-separated list of emails")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vendors_created"
    )
    unit = models.ForeignKey(
        "users.Unit",
        on_delete=models.CASCADE,
        related_name="vendors"
    )

    def __str__(self):
        return self.name




class Contract(models.Model):
    CURRENCY_CHOICES = [
        ('GHS', 'Ghana Cedis'),
        ('USD', 'US Dollars'),
    ]

    contract_number = models.CharField(
        max_length=100,
        primary_key=True,
        editable=False,
        unique=True
    )
    vendor = models.OneToOneField(
        Vendor,
        related_name='contract',
        on_delete=models.CASCADE
    )
    contract_start_date = models.DateField(null=True, blank=True)
    contract_expiry_date = models.DateField()
    contract_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    contract_terms = models.TextField()

    def save(self, *args, **kwargs):
        if not self.contract_number:
            vendor_slug = slugify(self.vendor.name).upper()
            self.contract_number = f"CTR-{vendor_slug}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Contract {self.contract_number} - {self.vendor.name}"




class Service(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    shortcode = models.CharField(max_length=50)
    revenue_share = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.vendor.name}"


class Contact(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='contacts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_numbers = models.TextField(help_text="Comma-separated list of phone numbers")
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.vendor.name}"


class Document(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='documents', on_delete=models.CASCADE)
    file = models.FileField(upload_to='vendor_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.vendor.name}"

