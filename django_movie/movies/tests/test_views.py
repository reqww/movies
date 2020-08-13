

import pytest
import requests
from django.urls import reverse
from django.conf import settings
from django.test import TestCase

# class TestViews(TestCase):

#     def test_product_detail_authenticated(self):
#         payload = {'username': 'reqww', 'password': 'CFHFYXF228hec;'}
#         path_to_token = settings.DJANGO_DOMEN + '/auth/token/login/'
#         r_token = requests.post(path_to_token, data=payload)
#         token = r_token.json()['auth_token']

#         path = settings.DJANGO_DOMEN + reverse('movie-detail', kwargs={'pk': 1})
#         headers = {'Authorization': f'Token {token}'}
#         r = requests.get(path, headers=headers)

#         assert r.status_code == 200

#     def test_product_detail_unauthenticated(self):
#         token = ''

#         path = settings.DJANGO_DOMEN + reverse('movie-detail', kwargs={'pk': 1})
#         headers = {'Authorization': f'Token {token}'}
#         r = requests.get(path, headers=headers)

#         assert r.status_code == 401

@pytest.fixture
def path():
    return settings.DJANGO_DOMEN + reverse('movie-detail', kwargs={'pk': 1})

@pytest.fixture
def token(request):
    return request.param

def get_token():
    payload = {'username': 'reqww', 'password': 'CFHFYXF228hec;'}
    path_to_token = settings.DJANGO_DOMEN + '/auth/token/login/'
    r_token = requests.post(path_to_token, data=payload)
    
    return r_token.json()['auth_token']

@pytest.mark.parametrize('token', [get_token()], indirect=True)
def test_product_detail_authenticated(path, token):
    path = path
    headers = {'Authorization': f'Token {token}'}
    r = requests.get(path, headers=headers)

    assert r.status_code == 200

@pytest.mark.parametrize('token', [''], indirect=True)
def test_product_detail_unauthenticated(path, token):
    path = path
    headers = {'Authorization': f'Token {token}'}
    r = requests.get(path, headers=headers)

    assert r.status_code == 401

