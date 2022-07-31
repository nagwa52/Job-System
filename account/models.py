from django.db import models
from django.contrib.auth.models import AbstractUser
from .validator import validate_file_extension
from tag.models import Tag


class User(AbstractUser):
    """
    user and company model
    """
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    TYPES = (
        ('admin', 'Admin'),
        ('recruiter', 'Recruiter'),
        ('developer', 'Developer'),
    )
    GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    type = models.fields.CharField(verbose_name="User Type", choices=TYPES, max_length=10)
    allow_mail_notification = models.BooleanField(default=True)
    gender = models.fields.CharField(verbose_name="Gender", choices=GENDER, max_length=1)
    date_of_birth = models.fields.DateField(verbose_name="Date of Birth")
    """
    Fields related to Developer (user_type)
    """
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    cv = models.FileField(verbose_name="CV", upload_to='media', validators=[validate_file_extension], null=True, blank=True)
    """
    Fields related to Recruiter (user_type)
    """
    address = models.fields.TextField(verbose_name="Address", null=True, blank=True)
    history = models.fields.TextField(verbose_name="Company History", null=True, blank=True)
    """
    AbstractUser Fields override
    """
    email = models.EmailField(verbose_name="Email Address", unique=True, max_length=50)
    is_active = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'password', 'gender', 'type', 'date_of_birth']

    def __str__(self):
        return self.username

