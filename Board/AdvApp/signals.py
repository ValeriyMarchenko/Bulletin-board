from django.db.models.signals import post_save

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from django.dispatch import receiver

from django.contrib.auth.models import User

from .models import Response, Advert


@receiver(post_save, sender=Response)
def notify(sender, instance, created, **kwargs):    
    if instance.accepted == True:
        user = instance.id_user

        html_content = render_to_string('mail_response.html', {'response': instance, })

        mail_subject = f'Hi {user}. Your respond on "{instance.id_advert|truncatechars:50}"... is now accepted!'

        msg = EmailMultiAlternatives(
            subject=mail_subject,
            body='',
            from_email='s44tpdude@yandex.ru',
            to=[user.email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
