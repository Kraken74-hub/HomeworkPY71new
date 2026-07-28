from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser, Event


@shared_task(name="send_email_task")
def send_email_task(subject, message, recipient_list):
    """Задача отправки email, работающая в отдельной очереди 'email'"""
    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@events.com',
        recipient_list=recipient_list,
        fail_silently=False,
    )


@shared_task
def send_event_reminders():
    """Периодическая задача: отправка напоминаний за день (24ч) и за 6 часов"""
    now = timezone.now()

    # 1. Напоминания за 24 часа (окно в 15 минут для точной сработки)
    tomorrow_start = now + timedelta(hours=24)
    events_24h = Event.objects.filter(
        meeting_time__gte=tomorrow_start,
        meeting_time__lt=tomorrow_start + timedelta(minutes=15)
    )
    for event in events_24h:
        recipients = list(event.users.filter(notify=True).values_list('email', flat=True))
        if recipients:
            msg = (f"Уведомляем вас, что вы согласились посетить «{event.name}».\n"
                   f"«{event.description}».\n"
                   f"Мероприятие проходит завтра в «{event.meeting_time}» «{event.place}».")
            send_email_task.delay("Напоминание о мероприятии", msg, recipients)

    # 2. Напоминания за 6 часов
    in_6h_start = now + timedelta(hours=6)
    events_6h = Event.objects.filter(
        meeting_time__gte=in_6h_start,
        meeting_time__lt=in_6h_start + timedelta(minutes=15)
    )
    for event in events_6h:
        recipients = list(event.users.filter(notify=True).values_list('email', flat=True))
        if recipients:
            msg = (f"Напоминание! До мероприятия «{event.name}» осталось 6 часов.\n"
                   f"Ждем вас в «{event.meeting_time}» по адресу «{event.place}».")
            send_email_task.delay("Скоро мероприятие!", msg, recipients)