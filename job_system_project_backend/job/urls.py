from django.urls import path
from .views import jobs_list, job_detail, job_search_list, create_job, update, apply, assign
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('list', jobs_list, name='list'),
    path('detail/<int:id>', job_detail, name='detail'),
    path('filtered', job_search_list, name='filtered'),
    path('create', create_job, name='enter_job'),
    path('update/<int:id>', update, name='update_status'),
    path('apply/<int:id>', apply, name='apply_to_job'),
    path('assign/<int:job_id>/<int:developer_id>', assign, name='assign_job'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
