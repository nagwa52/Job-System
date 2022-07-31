from django.db import models
from account.models import User
from .validator import validate_file_extension
from tag.models import Tag


class Job(models.Model):
    STATUS = (
        ('Open', 'Open'),
        ('Inprogress', 'Inprogress'),
        ('Finished', 'Finished'),
    )
    name = models.fields.CharField(verbose_name='Job Name', max_length=50)
    description = models.fields.CharField(verbose_name='Description', max_length=250)
    status = models.fields.CharField(choices=STATUS, max_length=40)
    Tags = models.ManyToManyField('tag.tag')
    applied_developer = models.ManyToManyField(User, related_name="applied_developer", null=True, blank=True)
    accepted_developer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accepted_developer", null=True,blank=True)
    banner_image = models.ImageField(upload_to='media', default='job.jpg')
    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by", null=True)
    
    def __str__(self):
        return self.name
