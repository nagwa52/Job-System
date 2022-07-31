from django.db import models


class Tag(models.Model):

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.fields.CharField(verbose_name="Tag Name", max_length=100, null=True)

    def __str__(self):
        return f"{self.name}"
