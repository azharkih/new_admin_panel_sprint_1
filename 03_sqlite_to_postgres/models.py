from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TimeStampedMixin(BaseModel):
    created: datetime
    modified: datetime

    class Config:
        fields = {
            'created': 'created_at',
            'modified': 'updated_at',
        }


class UUIDMixin(BaseModel):
    id: str


class PersonModel(TimeStampedMixin, UUIDMixin):
    full_name: str
    gender: Optional[str]


class FilmWorkModel(TimeStampedMixin, UUIDMixin):
    title: str
    description: Optional[str]
    creation_date: Optional[datetime]
    file_path: Optional[str]
    rating: Optional[float]
    certificate: Optional[str]
    type: str


class GenreModel(TimeStampedMixin, UUIDMixin):
    name: str
    description: Optional[str]


class GenreFilmWorkModel(UUIDMixin):
    film_work_id: str
    genre_id: str
    created: datetime

    class Config:
        fields = {'created': 'created_at'}


class PersonFilmWorkModel(UUIDMixin):
    film_work_id: str
    person_id: str
    role: str
    created: datetime

    class Config:
        fields = {'created': 'created_at'}


MOVIES_MODELS = {
    'film_work': FilmWorkModel,
    'genre': GenreModel,
    'genre_film_work': GenreFilmWorkModel,
    'person': PersonModel,
    'person_film_work': PersonFilmWorkModel,
}
