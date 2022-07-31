from rest_framework.permissions import BasePermission
from .models import Job


class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        if request.user.type == 'recruiter':
            return True
        else:
            return False


class IsDeveloper(BasePermission):
    def has_permission(self, request, view):
        def check_not_apply_before():
            applied_developer_ids = list(Job.objects.filter(status='Open').values_list('applied_developer', flat=True))
            print(applied_developer_ids)
            if request.user.id not in applied_developer_ids:
                return True
            else:
                print('applied to another job')
                return False

        if request.user.type == 'developer':
            if check_not_apply_before():
                return True
            else:
                return False
        else:
            return False








