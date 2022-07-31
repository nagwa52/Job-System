from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Job
from .models import Tag
from .serializers import JobSerializer
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from rest_framework.response import Response
from .permissions import IsRecruiter, IsDeveloper
from rest_framework.decorators import permission_classes
from account.models import User


@api_view(['GET'])
def jobs_list(request, format=None):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return JsonResponse({"jobs": serializer.data}, safe=False)


@api_view(['POST'])
@permission_classes([IsRecruiter])
def create_job(request, format=None):
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        job = serializer.save()
        job.Tags.set(request.data['Tags'].split(','))
        job.applied_developer.set(request.data.get('applied_developer'))
        job.accepted_developer_id = request.data.get('accepted_developer')
        job.created_by_id = request.user.id
        job.save()
        return Response("status: Job created successfully", status.HTTP_201_CREATED)
    return Response(status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def job_detail(request,id,format=None):
    try:
        job = Job.objects.get(pk=id)
    except Job.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobSerializer(job)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = JobSerializer(job, data=request.data)
        job.Tags.set(request.data['Tags'].split(','))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        if job.status == 'Open':
            job.delete()
            return JsonResponse({"status": "job is deleted successfully"}, status=status.HTTP_202_ACCEPTED)
        return JsonResponse({"status": "can't delete job of status In progress or finished"}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
def job_search_list(request):
    query = request.query_params.get('query')
    jobs = Job.objects.filter(Tags__in=[query])
    serializer = JobSerializer(jobs, many=True)
    return JsonResponse({"filtered jobs": serializer.data}, safe=False)


@api_view(['Get'])
def update(request, id):
    try:
        job = Job.objects.get(pk=id)
        if request.user == job.accepted_developer or request.user == job.created_by:
            if job.status == 'Inprogress':
                job.status = 'Finished'
                job.save()
                return Response("Job updated successfully", status=status.HTTP_200_OK)
            else:
                return Response("Job status should be Inprogress to be updated", status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("You Don't Have permission to do this action", status=status.HTTP_406_NOT_ACCEPTABLE)

    except Job.DoesNotExist:
        return Response("Job doesn't exist ", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsDeveloper])
def apply(request, id):
    try:
        job = Job.objects.get(pk=id)
        job_tags = list(Job.objects.filter(pk=id).values_list('Tags', flat=True))

        user_id = request.user.id
        developer_tags = list(User.objects.filter(pk=user_id).values_list('tags', flat=True))

        def isIncluded():
            for tag in job_tags:
                for item in developer_tags:
                    if tag == item:
                        return True

        if job.status == 'Open':
            if isIncluded():
                job.applied_developer.add(request.user)
                job.save()
                return Response("developer has been applied th this job", status=status.HTTP_200_OK)
            else:
                return Response("developer has no matching tags with job", status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("Job status is not Open", status=status.HTTP_406_NOT_ACCEPTABLE)

    except Job.DoesNotExist:
        return Response("Job doesn't exist ", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsRecruiter])
def assign(request, job_id, developer_id):
    try:
        job = Job.objects.get(pk=job_id)
        developer_ids = list(Job.objects.filter(pk=job_id).values_list('applied_developer', flat=True))
        if request.user == job.created_by and job.status == 'Open':
            if developer_id in developer_ids:
                job.accepted_developer = User.objects.get(id=developer_id)
                job.status = 'Inprogress'
                job.save()
                return Response("Success", status=status.HTTP_200_OK)
            else:
                return Response("Selected Developer is not one of the applied developers", status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("You are not the owner of this Job or Job status is not open", status=status.HTTP_406_NOT_ACCEPTABLE)
    except Job.DoesNotExist:
        return Response("Job doesn't exist ", status=status.HTTP_404_NOT_FOUND)
