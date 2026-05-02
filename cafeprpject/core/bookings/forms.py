from django import forms
from .models import Reservation
from django.utils import timezone


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'hour_start', 'hour_end']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        date = cleaned_data.get('date')
        start = cleaned_data.get('hour_start')
        end = cleaned_data.get('hour_end')
        user = self.user  # Передадим юзера в init или установим позже

        if not date or not start or not end:
            return cleaned_data

        # 1. Проверка на прошлое
        if date < timezone.now().date():
            raise forms.ValidationError("Нельзя забронировать на прошедшую дату.")

        # 2. Время работы 8:00 - 18:00
        if start < 8 or end > 18 or start >= end:
            raise forms.ValidationError("Кафе работает с 8:00 до 18:00. Проверьте часы.")

        # 3. Проверка занятости столика (пересечение интервалов)
        overlap = Reservation.objects.filter(
            table=table,
            date=date,
            hour_start__lt=end,
            hour_end__gt=start
        ).exists()
        if overlap:
            raise forms.ValidationError("Этот столик уже занят на выбранное время.")

        # 4. Ограничение: не более 3 броней на пользователя в день (доп. требование)
        user_daily_count = Reservation.objects.filter(user=user, date=date).count()
        if user_daily_count >= 3:
            raise forms.ValidationError("Вы не можете забронировать более 3 столиков на один день.")

        return cleaned_data