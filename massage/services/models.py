from django.db import models

class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('default', 'Обычная категория (без цены и кол-ва)'),
        ('with_price_and_sessions', 'С ценой и кол-вом сеансов'),
        ('with_price_only', 'Только цена, без фото и сеансов'),
    ]

    name = models.CharField("Название категории", max_length=200, db_index=True)
    slug = models.SlugField("URL-код", max_length=200, unique=True, db_index=True)
    type = models.CharField(
        "Тип отображения",
        max_length=32,
        choices=CATEGORY_TYPE_CHOICES,
        default='default'
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='services',
        verbose_name="Категория",
        on_delete=models.CASCADE
    )
    name = models.CharField("Название услуги/товара", max_length=200, db_index=True)
    slug = models.SlugField("URL-код", max_length=200, unique=True, db_index=True)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, null=True, blank=True)
    sessions_count = models.PositiveIntegerField("Количество сеансов", null=True, blank=True)
    available = models.BooleanField("В наличии/активно", default=True)
    created = models.DateTimeField("Добавлено", auto_now_add=True)
    updated = models.DateTimeField("Обновлено", auto_now=True)
    photo = models.ImageField("Фото услуги", upload_to='services/photos/', blank=True, null=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def __str__(self):
        return self.name


class ServiceDetail(models.Model):
    service = models.ForeignKey(
        Service,
        related_name='details',
        verbose_name="Основная услуга",
        on_delete=models.CASCADE
    )
    name = models.CharField("Название варианта услуги", max_length=200)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    session_time = models.DurationField("Время сеанса")  # хранит длительность, например 00:30:00 для 30 минут

    class Meta:
        verbose_name = "Вариант услуги"
        verbose_name_plural = "Варианты услуг"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.service.name})"
