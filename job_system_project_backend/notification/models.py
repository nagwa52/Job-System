from django.db import models
from account.models import User


class Notification(models.Model):

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    message = models.fields.TextField(verbose_name='message', null=False)
    created_at = models.fields.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.message}"


