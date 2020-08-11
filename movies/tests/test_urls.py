from django.urls import reverse, resolve

class TestUrls:

    def test_movie_detail_url(self):
        path = reverse('movie-detail', kwargs={'pk': 1})
        assert resolve(path).view_name == 'movie-detail'