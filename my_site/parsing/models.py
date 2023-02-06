import jsonfield
from django.db import models
from transliterate import slugify


def default_urls():
    return {'hh_work', '', 'habr_work', '', 'superjob_work', ''}


class City(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Language(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            sl = slugify(self.title)
            if sl:
                self.slug = sl
            else:
                self.slug = self.title.lower()
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    language = models.ForeignKey('Language', on_delete=models.PROTECT, verbose_name='Язык программирования')
    company = models.CharField(max_length=255, verbose_name='Компания')
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='Город')
    description = models.TextField(blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    url = models.URLField(unique=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-time_create']

    def __str__(self):
        return self.title


class Error(models.Model):
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    data = jsonfield.JSONField()

    class Meta:
        verbose_name = 'Ошибка'
        verbose_name_plural = 'Ошибки'

    def __str__(self):
        return str(self.time_create)


class Url(models.Model):
    language = models.ForeignKey('Language', on_delete=models.PROTECT, verbose_name='Язык программирования')
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='Город')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'language')

    def __str__(self):
        return f'{self.language} - {self.city}'
