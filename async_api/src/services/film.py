from functools import lru_cache

from core.config import settings
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Film

from services.base import BaseService
from state.state import State, get_storage


class FilmService(BaseService):
    def __init__(self, state: State, elastic: AsyncElasticsearch):
        super().__init__(state, elastic)
        self.index = "movies"
        self.expire = settings.FILM_CACHE_EXPIRE_IN_SECONDS
        self.model = Film


@lru_cache()
def get_film_service(
    state: State = Depends(get_storage),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> BaseService:
    return FilmService(state, elastic)
