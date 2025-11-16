from django.db import models

class Booking(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")

    date = models.DateField(verbose_name="Дата сеанса")
    time = models.TimeField(verbose_name="Время сеанса")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий к записи")

    class Meta:
        unique_together = ('date', 'time')
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"
