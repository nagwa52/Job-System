from django.urls import path
from notification import views

app_name = "notification"

urlpatterns = [
    path('list', views.list_user_notifications),
]
