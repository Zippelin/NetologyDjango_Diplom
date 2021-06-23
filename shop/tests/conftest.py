import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def products_factory():
    def factory(**kwargs):
        return baker.make('products.Product', **kwargs)
    return factory


@pytest.fixture
def reviews_factory():
    def factory(**kwargs):
        return baker.make('reviews.Review', **kwargs)
    return factory


@pytest.fixture
def orders_factory():
    def factory(**kwargs):
        return baker.make('orders.Order', make_m2m=True, **kwargs)
    return factory


@pytest.fixture
def collections_factory():
    def factory(**kwargs):
        return baker.make('collections_.Collection', make_m2m=True, **kwargs)
    return factory


@pytest.fixture
def user_factory():
    def factory(**kwargs):
        if kwargs['is_superuser'] == True:
            return get_user_model().objects.get(username="admin")
        elif kwargs['is_superuser'] == False:
            return get_user_model().objects.create(username="user", password="user", email="user@user.com")
        else:
            return get_user_model().objects.create(username="user", password="user", email="user@user.com", is_active=False)
    return factory


@pytest.fixture
def token_factory():
    def factory(**kwargs):
        if kwargs['user'].is_active:
            return Token.objects.create(user=kwargs['user']).key
        else:
            return ''
    return factory