from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

COLOR_CHOICES = [
    ('MediumSeaGreen', 'Зеленый'),
    ('PaleVioletRed', 'Красный'),
    ('Khaki', 'Желтый'),
    ('Plum', 'Фиолетовый'),
    ('SkyBlue', 'Синий'),
    ('LightSlateGray', 'Серый'),
]


class Note(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    text = models.TextField(blank=True, null=True, max_length=300)
    theme = models.ForeignKey('Theme', blank=True, null=True, related_name='notes', on_delete=models.CASCADE,
                              verbose_name='Тема')
    author = models.ForeignKey('Profile', blank=True, null=True, related_name='notes', on_delete=models.CASCADE,
                               verbose_name='Автор')
    importance = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)],
                                     verbose_name='Важность')
    color = models.CharField(max_length=30, choices=COLOR_CHOICES, default='green', verbose_name='Цвет')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Запись активна')

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['importance', '-created']

    def __str__(self):
        return self.title

    def soft_delete(self):
        self.is_active = False
        self.save()


class Theme(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название темы')

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.title

    def count_notes(self):
        return self.notes.count()


class Profile(models.Model):
    def validate_image(fieldfile_obj):
        file_size = fieldfile_obj.file.size
        megabyte_limit = 150.0
        if file_size > megabyte_limit * 1024 * 1024:
            raise ValidationError(
                "Максимальный размер файла {}MB".format(str(megabyte_limit))
            )

    user = models.OneToOneField(
        User, unique=True, on_delete=models.CASCADE, related_name="profile"
    )

    username = models.CharField(
        default="-------",
        max_length=50,
        verbose_name="Имя пользователя",
        blank=True,
        null=True,
        unique=False,
    )

    avatar = models.ImageField(
        upload_to="catalog/files/",
        null=True,
        validators=[validate_image],
        default="catalog/files/ava-default.png",
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return self.username

    def count_notes(self):
        return self.notes.count()
