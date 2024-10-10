from django.db import models

from base.constants import RequestStatusChoices, CostTypeChoices
from base.models import BaseModel


# Create your models here.


class Project(BaseModel):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='owned_projects')
    subsidiary = models.ForeignKey('organization.Subsidiary', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ExpenditureRequest(BaseModel):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='created_requests')
    version = models.PositiveIntegerField(default=1)
    cost_low = models.DecimalField(max_digits=15, decimal_places=2)
    cost_high = models.DecimalField(max_digits=15, decimal_places=2)
    cost_base = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey('organization.Currency', on_delete=models.SET_DEFAULT, default='USD')
    scope_of_work = models.TextField()
    duration = models.DurationField(blank=True, null=True)
    cost_type = models.CharField(max_length=50, choices=CostTypeChoices.choices)
    status = models.CharField(max_length=50, choices=RequestStatusChoices.choices, default=RequestStatusChoices.PENDING)
    assets = models.ManyToManyField('Asset', through='ExpenditureRequestAsset', blank=True)

    def __str__(self):
        return f"Request {self.id} - {self.project.name}"


class ExpenditureRequestAsset(BaseModel):
    request = models.ForeignKey('ExpenditureRequest', on_delete=models.CASCADE)
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('request', 'asset')

    def __str__(self):
        return f"Asset {self.asset} in Request {self.request}"


class ApprovalWorkflowStep(BaseModel):
    step_number = models.PositiveIntegerField()
    step_name = models.CharField(max_length=100)
    approval = models.ForeignKey('Approval', on_delete=models.CASCADE, related_name="workflows")
    approval_officer = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name="approval_workflows")
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


class RequestAttachment(BaseModel):
    request = models.ForeignKey('ExpenditureRequest', on_delete=models.CASCADE)
    scenario = models.ForeignKey('BusinessScenario', on_delete=models.CASCADE)
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE, blank=True, null=True)
    uploaded_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name


class RequestHistory(BaseModel):
    request = models.ForeignKey('ExpenditureRequest', on_delete=models.CASCADE, related_name='histories')
    version = models.PositiveIntegerField()
    modified_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True)
    cost_low = models.DecimalField(max_digits=15, decimal_places=2)
    cost_high = models.DecimalField(max_digits=15, decimal_places=2)
    cost_base = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True)
    scope_of_work = models.TextField()
    duration = models.CharField(max_length=100, blank=True, null=True)
    cost_type = models.CharField(max_length=50, choices=CostTypeChoices.choices)
    status = models.CharField(max_length=50, choices=RequestStatusChoices.choices)
    assets = models.ManyToManyField('Asset', blank=True)

    def __str__(self):
        return f"Version {self.version} of Request {self.request.id}"


class RequestComment(BaseModel):
    request = models.ForeignKey('ExpenditureRequest', on_delete=models.CASCADE, blank=True, null=True)
    approval = models.ForeignKey('Approval', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at}"
