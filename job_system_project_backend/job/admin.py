from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin (admin.ModelAdmin):
    list_filter = ('name', 'status',)
    search_fields = ['applied_developer__username', 'accepted_developer__username', 'created_by__username']
    list_display = ['name', 'description', 'status', 'creation_time', 'update_time', 'All_Tags', 'created_by','Applied_Developers', 'accepted_developer']

    def Applied_Developers(self, obj):
        if obj.applied_developer.all():
            return list(obj.applied_developer.all().values_list('username', flat=True))
        else:
            return 'NA'

    def All_Tags(self, obj):
        if obj.Tags.all():
            return list(obj.Tags.all().values_list('name', flat=True))
        else:
            return 'NA'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

