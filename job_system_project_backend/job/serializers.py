from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    # inner class called meta to describe data of the model
    class Meta:
        model = Job
        fields = ['id', 'name', 'description', 'status', 'creation_time', 'update_time', 'Tags', 'applied_developer',
'accepted_developer',
'banner_image',
'created_by']

    # we use serializers when we want to return our model to the api
    # we use serializers when we want to return our model to the api
        # model = Job
        # fields = '__all__'
        depth = 1
