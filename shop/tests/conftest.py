import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def products_factory():
    def factory(**kwargs):
        return baker.make('products.Product', **kwargs)
    return factory