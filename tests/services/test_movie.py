from unittest.mock import MagicMock
import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService

from setup_db import db


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    movie1 = Movie(id=1, title='test_movie1', description='test_description1', trailer='tr', year=2000, rating=5, genre_id=1, director_id=1)
    movie2 = Movie(id=2, title='test_movie2', description='test_description2', trailer='tr', year=2000, rating=5, genre_id=1, director_id=1)
    movie3 = Movie(id=3, title='test_movie3', description='test_description3', trailer='tr', year=2000, rating=5, genre_id=1, director_id=1)

    movie_dao.get_one = MagicMock(return_value=movie1)
    movie_dao.get_all = MagicMock(return_value=[movie1, movie2, movie3])
    movie_dao.create = MagicMock(return_value=Movie(id=2))
    movie_dao.update = MagicMock()
    movie_dao.delete = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        new_movie = {
            "title": "new_movie"
        }
        movie = self.movie_service.create(new_movie)
        assert movie.id != None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        update_movie = {
            "title": "update_movie"
        }
        self.movie_service.update(update_movie)



