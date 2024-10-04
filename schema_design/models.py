from django.db import models


class RequestStatus(models.TextChoices):
    PENDING = 'Pending'
    APPROVED = 'Approved'


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Permission(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=(
                'name',
            )),
        ]

    def __str__(self):
        return self.name


class Role(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')

    class Meta:
        indexes = [
            models.Index(fields=(
                'name'
            )),
        ]

    def __str__(self):
        return self.name


class User(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    roles = models.ManyToManyField(Role, related_name="users")

    class Meta:
        indexes = [
            models.Index(fields=(
                'email',
                'created_at',
            )),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ExpenditureRequest(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    scope = models.CharField(max_length=255)
    amount = models.FloatField()
    raised_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="expenditure_requests")
    status = models.CharField(max_length=20, choices=RequestStatus.choices, default=RequestStatus.PENDING)

    class Meta:
        indexes = [
            models.Index(fields=(
                'amount',
                'created_at',
                'raised_by',
                'status',
            )),
        ]

    def __str__(self):
        return self.title


class ApprovalWorkflow(BaseModel):
    level = models.PositiveIntegerField()
    approval = models.ForeignKey('Approval', on_delete=models.CASCADE, related_name="workflows")
    approval_officer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="approval_workflows")
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            'level',
            'approval',
        )
        indexes = [
            models.Index(fields=(
                'created_at',
                'level',
                'approval',
                'approval_officer',
                'is_approved',
            )),
        ]

    def __str__(self):
        return f"Workflow Level {self.level} for {self.approval}"


class Approval(BaseModel):
    request = models.OneToOneField(ExpenditureRequest, on_delete=models.CASCADE, related_name="approvals")
    is_completed = models.BooleanField(default=False)
    completed_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=(
                'created_at',
                'request',
                'workflow',
                'is_completed'
            )),
        ]

    def __str__(self):
        return f"Approval for Request {self.request_id}"
