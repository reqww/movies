from mixer.backend.django import mixer
import pytest

@pytest.mark.django_db
class TestModels:

    def test_movie_str(self):
        movie = mixer.blend('movies.Movie', title = 'movie')
        assert str(movie) == 'movie'