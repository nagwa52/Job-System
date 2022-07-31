from django.urls import path

from tag import views

app_name = "tag"


urlpatterns = [
    path('list', views.list_tags),
]
