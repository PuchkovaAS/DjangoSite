import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from .my_data import transliterate


class UserLocation(models.Model):
    BOOTSTRAP4_STYLE = [
        ('badge rounded-pill bg-primary', 'синий'),
        ('badge rounded-pill bg-secondary', 'серый'),
        ('badge rounded-pill bg-success', 'зеленый'),
        ('badge rounded-pill bg-info text-dark', 'голубой'),
        ('badge rounded-pill bg-warning text-dark', 'желтый'),
        ('badge rounded-pill bg-danger', 'красный'),
        ('badge rounded-pill bg-light text-dark', 'светлый'),
        ('badge rounded-pill bg-dark', 'темный')

    ]
    location = models.CharField("Местоположение пользователя", max_length=200, unique=True)
    loc_description = models.TextField("Описание местоположение", blank=True, null=True)
    loc_class = models.CharField("Класс bootstrap", max_length=200, choices=BOOTSTRAP4_STYLE,
                                 default='badge badge-pill bg-dark')

    def table_class(self):
        return self.loc_class.split('bg-')[-1].split(' ')[0]

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

    # description = models.TextField("Описание события", null=True, blank=True)

    class Meta:
        # критерии сортировки
        ordering = ['-user.username']

    def get_full_name(self):
        return f"{self.user.last_name} {self.user.first_name} {self.father_name}"

    def get_short_name(self):
        return f"{self.user.last_name} {self.user.first_name[0]}. {self.father_name[0]}."

    # def save(self, *args, **kwargs):
    #     self.pub_date = timezone.now().date()
    #     return super(Profile, self).save(*args, **kwargs)

    # def whenpublished(self):
    #     now = timezone.now().date()
    # 
    #     diff = now - self.pub_date
    # 
    #     if diff.days == 0:
    #         return "Сегодня"
    #     if diff.days == 1:
    #         return "1 день назад"
    #     if diff.days < 5:
    #         return f"{diff.days} дня назад"
    # 
    #     return f"{diff.days} дней назад"

    def get_absolute_url(self):
        """генерирует ссылку вместо {% url 'post_detail_url' slug=post.slug%}"""
        return reverse('user_detail', kwargs={'slug': self.url})

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.father_name}"

    def save(self, *args, **kwargs):
        self.url = slugify(str(self.user.username).lower() + str(self.tabel_num))
        super(Profile, self).save()

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Project(models.Model):
    STATUS_PROJECT = [
        ('Не начат', 'Не начат'),
        ('Подготовка', 'Подготовка'),
        ('В работе', 'В работе'),
        ('Сдан', 'Сдан'),
        ('Тех. обслуживание', 'Тех. обслуживание'),
    ]

    STATUS_STYLE_PROJECT = {
        'Не начат': 'badge bg-danger',
        'Подготовка': 'badge bg-secondary',
        'В работе': 'badge bg-primary',
        'Сдан': 'badge bg-success',
        'Тех. обслуживание': 'badge bg-warning text-dark',
    }

    name = models.CharField("Название", max_length=200, blank=False, null=False, unique=True)

    status = models.CharField("Статус проекта", max_length=200, choices=STATUS_PROJECT,
                              default='Не начат')

    # staff = models.ManyToManyField(AgentProject, verbose_name='Инагент', blank=True, related_name='Инагенты')
    # staff
    description = models.TextField("Описание события", null=True, blank=True)
    tasks = models.TextField("Задачи", max_length=2000, blank=True, null=True)

    url = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", default=None, null=True,
                           blank=True)

    class Meta:
        # критерии сортировки
        ordering = ['-name']

    def status_style(self):
        return self.STATUS_STYLE_PROJECT[self.status]

    def get_absolute_url(self):
        """генерирует ссылку вместо {% url 'post_detail_url' slug=post.slug%}"""
        return reverse('project_detail', kwargs={'slug': self.url})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.url = slugify(f"{transliterate(str(self.name).lower())}")
        super(Project, self).save()

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class UserStatistic(models.Model):
    user_name = models.ForeignKey(Profile, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True)
    user_location = models.ForeignKey(UserLocation, verbose_name="Местоположение пользователя",
                                      on_delete=models.SET_NULL, null=True)
    description = models.TextField("Описание события", null=True, blank=True)
    pub_date = models.DateField('Время события', default=datetime.date.today, blank=False, null=False)
    project = models.ForeignKey(Project, verbose_name="Проект",
                                on_delete=models.SET_NULL, blank=True, null=True, related_name='user')

    def __str__(self):

        return f"{self.user_name.user.last_name} {self.user_name.user.first_name} {self.user_name.father_name} - {self.user_location}"

    class Meta:
        verbose_name = "Статистика пользователя"
        verbose_name_plural = "Статистика пользователей"
        ordering = ['-pub_date', '-id']

    def date_format(self):
        return f"{self.pub_date.strftime('%d-%m-%Y')}"

    def when_add(self):
        now = timezone.now().date()

        diff = now - self.pub_date

        if diff.days == 0:
            return "Сегодня"
        if diff.days == 1:
            return "1 день назад"
        if diff.days < 5:
            return f"{diff.days} дня назад"

        return f"{diff.days} дней назад"


class AgentProject(models.Model):
    first_name = models.CharField("Имя", max_length=200, blank=False, null=False)
    last_name = models.CharField("Фамилия", max_length=200, blank=False, null=False)
    father_name = models.CharField("Отчество", max_length=200, blank=False, null=False)

    position = models.CharField(verbose_name="Должность", max_length=200)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    location = models.ManyToManyField(Project, verbose_name='Объект', blank=True, related_name='agents')
    # related_name для связи many to many чтобы найти по тегу все посты
    phone_number = models.CharField(verbose_name='Телефон', max_length=200, blank=True, null=True)
    email = models.EmailField(verbose_name='Почта', blank=True, null=True)

    url = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", default=None, null=True,
                           blank=True)

    class Meta:
        # критерии сортировки
        verbose_name = "История проекта"
        verbose_name_plural = "Истории проекта"
        ordering = ['-second_name', '-first_name', '-father_name']

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.father_name}"

    def get_short_name(self):
        return f"{self.last_name} {self.first_name[0]}. {self.father_name[0]}."

    def get_absolute_url(self):
        """генерирует ссылку вместо {% url 'post_detail_url' slug=post.slug%}"""
        return reverse('agent_detail', kwargs={'slug': self.url})

    def __str__(self):
        return f"{str(self.last_name)} {str(self.first_name)} {str(self.father_name)}"

    def save(self, *args, **kwargs):
        self.url = slugify(
            f"{transliterate(str(self.last_name).lower())}_{transliterate(str(self.first_name).lower())}_{transliterate(str(self.father_name).lower())}_{datetime.datetime.now().microsecond}")
        super(AgentProject, self).save()

    class Meta:
        verbose_name = "Инагент"
        verbose_name_plural = "Инагенты"


class HistoryProject(models.Model):
    project = models.ForeignKey(Project, verbose_name="Проект", on_delete=models.SET_NULL, null=True,
                                related_name='history')
    pub_date = models.DateField('Время события', default=datetime.date.today, blank=False, null=False)
    user_add = models.ForeignKey(Profile, verbose_name="Сотрудник", on_delete=models.SET_NULL, null=True,
                                 related_name='users')
    description = models.TextField("Описание", null=True, blank=True)

    def __str__(self):
        return self.project.name

    class Meta:
        verbose_name = "История проекта"
        verbose_name_plural = "Истории проекта"
        ordering = ['-pub_date', '-id']

    def when_add(self):
        now = timezone.now().date()

        diff = now - self.pub_date

        if diff.days == 0:
            return "Сегодня"
        if diff.days == 1:
            return "1 день назад"
        if diff.days < 5:
            return f"{diff.days} дня назад"

        return f"{diff.days} дней назад"
