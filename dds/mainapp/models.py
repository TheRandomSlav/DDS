from django.db import models

# Create your models here.

# Модель для хранения статусов
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Статус')

    def __str__(self):
        return self.name

# Модель для хранения типов
class Type(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Тип')

    def __str__(self):
        return self.name

# Модель для категорий
class Category(models.Model):
    type = models.ForeignKey(Type, related_name='categories', null=True,  on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, verbose_name='Категория')

    def __str__(self):
        return self.name

# Модель для подкатегорий
class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Подкатегория')

    class Meta:
        unique_together = ('category', 'name')
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return f"{self.category.name} - {self.name}"

# Основная модель записи
class Record(models.Model):
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания записи',
        help_text='Заполняется автоматически, но может быть изменена вручную.'
    )

    created_at = models.DateTimeField(
        verbose_name='Дата создания записи'
    )

    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name='Тип')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    subcategory = models.ForeignKey(Subcategory, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Подкатегория')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма в рублях')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return f"{self.created_at.date()} - {self.amount} руб."