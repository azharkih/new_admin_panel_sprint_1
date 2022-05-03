import uuid

from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='genre_name_idx'),
        ]


class FilmWork(UUIDMixin, TimeStampedMixin):
    class FilmType(models.TextChoices):
        TV_SHOW = 'tv_show', _('tv_show')
        MOVIE = 'movie', _('movie')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'))
    rating = models.FloatField(
        _('rating'), blank=True, validators=[
            MinValueValidator(0), MaxValueValidator(100)
        ]
    )
    type = models.CharField(
        _('type'), max_length=10, choices=FilmType.choices,
        default=FilmType.MOVIE,
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    certificate = models.CharField(_('certificate'), max_length=512, null=True,
                                   blank=True)
    file_path = models.FileField(
        _('file'), blank=True, null=True, upload_to='movies/'
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = _('film_work')
        verbose_name_plural = _('film_works')
        indexes = [
            models.Index(fields=['creation_date'],
                         name='film_work_creation_date_idx'),
        ]


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"genre_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'genre'],
                name='film_work_genre_idx'),
        ]


class Gender(models.TextChoices):
    MALE = 'male', _('male')
    FEMALE = 'female', _('female')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full_name'))
    gender = models.TextField(_('gender'), choices=Gender.choices, null=True)
    film_works = models.ManyToManyField(FilmWork, through='PersonFilmWork')

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content\".\"person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class PersonFilmWork(models.Model):
    class PersonRoles(models.TextChoices):
        ACTOR = 'actor', _('actor')
        WRITER = 'writer', _('writer')
        DIRECTOR = 'director', _('director')

    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(
        _('Role'), max_length=10, choices=PersonRoles.choices,
        default=PersonRoles.ACTOR,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"person_film_work'

        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person', 'role'],
                name='film_work_person_idx'),
        ]
