from django.contrib import admin
from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline,)
    # Отображение полей в списке
    list_display = (
        'title', 'type', 'creation_date', 'rating', 'created', 'modified'
    )

    # Фильтрация в списке
    list_filter = ('type',)

    # Поиск по полям
    search_fields = ('title', 'description', 'id')


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmWorkInline,)

    # Отображение полей в списке
    list_display = ('full_name',)

    # Поиск по полям
    search_fields = ('full_name',)
