from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class UserLocation(models.Model):
    location = models.CharField("Местоположение пользователя", max_length=200, unique=True)
    loc_description = models.TextField("Описание местоположение")
    loc_class = models.CharField("Класс bootstrap", max_length=200)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    father_name = models.CharField("Отчество", max_length=200, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="День рождения")
    position = models.CharField("Должность", max_length=200)
    user_location = models.ForeignKey(UserLocation, verbose_name="Местоположение пользователя",
                                      on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UserStatistic(models.Model):
    user_name = models.OneToOneField(Profile, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True)
    user_location = models.ForeignKey(UserLocation, verbose_name="Местоположение пользователя",
                                      on_delete=models.SET_NULL, null=True)
    description = models.TextField("Описание события", null=True, blank=True)
    pub_date = models.DateTimeField('Время публикации', default=datetime.now())

    def __str__(self):
        return self.user_name.user.username

    class Meta:
        verbose_name = "Статистика пользователя"
        verbose_name_plural = "Статистика пользователей"
