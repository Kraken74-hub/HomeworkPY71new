from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Event
from .tasks import send_email_task


@receiver(post_save, sender=Event)
def notify_users_on_new_event(sender, instance, created, **kwargs):
    if created:
        subscribers = CustomUser.objects.filter(notify=True).values_list('email', flat=True)
        recipients = list(subscribers)

        if recipients:
            subject = f"Новое мероприятие: «{instance.name}»!"
            message = (
                f"Новое мероприятие: «{instance.name}»!\n"
                f"«{instance.description}».\n"
                f"Мероприятие проходит в «{instance.meeting_time}» «{instance.place}»."
            )
            send_email_task.delay(subject, message, recipients)