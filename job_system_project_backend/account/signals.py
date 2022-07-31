from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User
from django.core.mail import send_mail
from .api.v1.views import signup


@receiver(post_save, sender=User)
def account_signup_action(*args, **kwargs):
    if kwargs.get('created'):
        subject = 'New User Created'
        receivers = ['hadeermostafa.094@gmail.com']
        obj = kwargs.get('instance')
        current_user = obj.username
        msg = f"New User has been signed up recently, Please activate {current_user}'s Profile"
        res = send_mail(subject=subject, message=msg, from_email='djangonotifysys@gmail.com', recipient_list=receivers, fail_silently=False)
        print(res)

