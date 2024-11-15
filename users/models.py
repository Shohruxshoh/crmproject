from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re


# Create your models here.

class Region(models.Model):
    title = models.CharField('Имя', max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Провинция'
        verbose_name_plural = 'Провинции'


class District(models.Model):
    title = models.CharField('Имя', max_length=255)
    region = models.ForeignKey(Region, verbose_name='Провинция', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Районы'
        verbose_name_plural = 'Районы'


def validate_russian_phone_number(value):
    # Rossiya telefon raqami formati: +7 bilan boshlanib, 10ta raqam bo'lishi kerak.
    if not re.match(r'^\+7\d{10}$', value):
        raise ValidationError('Номер телефона должен начинаться с +7 и содержать 10 цифр.')


ADMIN = 1
OPERATOR = 2
MANAGER = 3

ROLE = (
    (ADMIN, 'Администратор'),
    (OPERATOR, 'Оператор'),
    (MANAGER, 'Менеджер')
)


class User(AbstractUser):
    role = models.IntegerField(verbose_name='Роль пользователя', choices=ROLE, default=OPERATOR)
    first_name = models.CharField(verbose_name='Имя', max_length=200)
    telegram = models.CharField(verbose_name='Telegram', max_length=200)
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=12,
        validators=[validate_russian_phone_number],
        help_text="Номер телефона должен начинаться с +7 и содержать 10 цифр.", unique=True
    )
    percentage = models.PositiveIntegerField('процент', default=0)
    region = models.ForeignKey(Region, verbose_name='Провинция', on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, verbose_name='Район', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'  # Telefon raqamni unique identifikator sifatida foydalanish
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
