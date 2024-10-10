from django.db import models


class AssetStatusChoices(models.TextChoices):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    DISPOSED = 'Disposed'


class CostTypeChoices(models.TextChoices):
    CAPEX = 'CAPEX'  # Capital Expenditure
    OPEX = 'OPEX'  # Operating Expenditure


class RequestStatusChoices(models.TextChoices):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
