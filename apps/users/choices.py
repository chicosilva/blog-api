from django.db.models import TextChoices


class UserType(TextChoices):
    ADMIN = "admin", "Admin"
    COMPANY = "company", "Company"
    CUSTOMER = "customer", "Customer"
