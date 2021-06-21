import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def orders_factory():
    def factory(**kwargs):
        return baker.make('Order', **kwargs)
    return factory