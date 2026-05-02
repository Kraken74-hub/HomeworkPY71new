from django.db import models
from django.contrib.auth.models import User

class Table(models.Model):
    number = models.IntegerField(unique=True, verbose_name="Номер столика")
    image = models.ImageField(upload_to='tables/', verbose_name="Изображение")
    seats = models.IntegerField(verbose_name="Количество мест")

    def str(self):
        return f"Столик №{self.number} ({self.seats} мест)"

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата бронирования")
    hour_start = models.IntegerField(verbose_name="Час начала")
    hour_end = models.IntegerField(verbose_name="Час окончания")
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Бронь столика №{self.table.number} пользователем {self.user.username}"
