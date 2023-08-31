from django.db import models
from django.core.validators import RegexValidator


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class JobPost(models.Model):
    refererId = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    designation = models.CharField(max_length=100)
    jobPostingDate = models.DateField(null=True, default=None)
    responsibilities = models.TextField()
    qualifications = models.TextField()
    experience = models.IntegerField()

    def __str__(self):
        return self.designation
