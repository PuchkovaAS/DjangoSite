from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils import timezone as django_tz
from django.utils.text import slugify


class UserLocation(models.Model):
    location = models.CharField("Местоположение пользователя", max_length=200, unique=True)
    loc_description = models.TextField("Описание местоположение", blank=True, null=True)
    loc_class = models.CharField("Класс bootstrap", max_length=200)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    father_name = models.CharField("Отчество", max_length=200, blank=True, null=True)
    tabel_num = models.IntegerField(verbose_name="Табельный номер", default=0)
    position = models.CharField("Должность", max_length=200)
    user_location = models.ForeignKey(UserLocation, verbose_name="Местоположение пользователя",
                                      on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", default=None, null=True,
                           blank=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    description = models.TextField("Описание события", null=True, blank=True)
    pub_date = models.DateField('Время изменения', default=django_tz.now)

    def save(self, *args, **kwargs):
        self.pub_date = timezone.now().date()
        return super(Profile, self).save(*args, **kwargs)

    def whenpublished(self):
        now = timezone.now().date()

        diff = now - self.pub_date

        if diff.days == 0:
            return "Сегодня"
        if diff.days == 1:
            return "1 день назад"
        if diff.days < 5:
            return f"{diff.days} дня назад"

        return f"{diff.days} дней назад"

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.url = slugify(str(self.user.username).lower() + str(self.tabel_num))
        super(Profile, self).save()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UserStatistic(models.Model):
    user_name = models.OneToOneField(Profile, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True)
    user_location = models.ForeignKey(UserLocation, verbose_name="Местоположение пользователя",
                                      on_delete=models.SET_NULL, null=True)
    description = models.TextField("Описание события", null=True, blank=True)
    pub_date = models.DateTimeField('Время публикации', auto_now_add=True)

    def __str__(self):
        return self.user_name.user.username

    class Meta:
        verbose_name = "Статистика пользователя"
        verbose_name_plural = "Статистика пользователей"
