from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.mail import send_mail
from tag.models import Tag
from .models import Job
from account.models import User
from notification.models import Notification


def job_creation_action(sender, **kwargs):
    obj = kwargs.get('instance')
    if kwargs.get('action') == 'post_add':
        tag_set = kwargs.get("pk_set")
        tag_id = tag_set.pop()
        tag = Tag.objects.get(pk=tag_id)
        developers = User.objects.filter(tags=tag).distinct()
        print(developers)
        for developer in developers:
            job_message = f"New job '{obj.name}' has been posted related to your subscribed tags, Check it out!"
            id = developer.id
            notify = Notification(message=job_message, user_id=id)
            notify.save()
            print("notification saved")
            if developer.allow_mail_notification == True:
                mail = developer.email
                subject = 'New Job has been posted!'
                receivers = ['hadeermostafa.094@gmail.com', mail]
                res = send_mail(subject=subject, message=job_message, from_email='djangonotifysys@gmail.com',
                                recipient_list=receivers, fail_silently=False)
                print("Email Sent Successfully!")
            else:
                pass


m2m_changed.connect(job_creation_action, sender=Job.Tags.through)


@receiver(post_save, sender=Job)
def job_assignment_action(*args, **kwargs):
    if kwargs.get('created') == False:
        obj = kwargs.get('instance')
        print(obj)
        if obj.accepted_developer is not None:
            accepted_developer_username = obj.accepted_developer
            print(accepted_developer_username)
            accepted_developer = User.objects.get(username=accepted_developer_username)
            print(accepted_developer)
            job_name = obj.name
            job_creator = obj.created_by
            job_message = f"You have been accepted for the job '{job_name}' created by '{job_creator}'"
            id = accepted_developer.id
            notify = Notification(message=job_message, user_id=id)
            notify.save()
            print("notification saved")
            if accepted_developer.allow_mail_notification == True:
                mail = accepted_developer.email
                subject = f"You have been accepted for the job '{job_name}'!"
                receivers = ['hadeermostafa.094@gmail.com', mail]
                res = send_mail(subject=subject, message=job_message, from_email='djangonotifysys@gmail.com',
                                recipient_list=receivers, fail_silently=False)
                print("Acceptance Email Sent Successfully!")


@receiver(post_save, sender=Job)
def job_update_action(*args, **kwargs):
    print(kwargs)
    if kwargs.get('created') == False:
        obj = kwargs.get('instance')
        job_owner = obj.created_by
        job_owner_obj = User.objects.get(username=job_owner)
        print(job_owner_obj.allow_mail_notification)
        if obj.status == 'Finished':
            print(obj.status)
            msg = f"Check {obj.name} Job, it has been marked as finished"
            id = job_owner.id
            notify = Notification(message=msg, user_id=id)
            notify.save()
            if job_owner_obj.allow_mail_notification == True:
                subject = 'Job has been finished'
                mail = job_owner_obj.email
                receivers = ['hadeermostafa.094@gmail.com', mail]
                res = send_mail(subject=subject, message=msg, from_email='djangonotifysys@gmail.com',
                                recipient_list=receivers, fail_silently=False)
                print(res)
            else:
                pass
        else:
            print('job not finished')
    else:
        pass
