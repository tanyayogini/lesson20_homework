from unittest.mock import MagicMock

import pytest
from dao.model.director import Director
from dao.director import DirectorDAO
from service.director import DirectorService

from setup_db import db


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)
    test_director1 = Director(id=1, name='test_director1')
    test_director2 = Director(id=2, name='test_director2')
    test_director3 = Director(id=3, name='test_director3')

    director_dao.get_one = MagicMock(return_value=test_director1)
    director_dao.get_all = MagicMock(return_value=[test_director1, test_director2, test_director3])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.update = MagicMock()
    director_dao.delete = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id == 1

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        new_director = {'name': 'new_director'}
        director = self.director_service.create(new_director)
        assert director.id == 3

    def test_update(self):
        update_director = {'name': 'update_director'}
        self.director_service.update(update_director)

    def test_delete(self):
        director = self.director_service.delete(3)
        assert director is None
