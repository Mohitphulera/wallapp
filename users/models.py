from django.contrib.auth.models import AbstractUser
from django.core import mail
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    pass


@receiver(post_save, sender=User)
def send_success_email(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        email = mail.EmailMessage('Welcome to TSL\'s Wall App!',
                                '%s, We\'re really pleased that you decided to join our website! '
                                ' Thanks!' % user.username,
                                'welcome@wall-app.com',
                                [user.email])
        email.send()
