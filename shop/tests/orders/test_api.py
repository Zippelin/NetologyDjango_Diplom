import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK


@pytest.mark.django_db
def test_products_list(api_client):
    url = reverse('product-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_product_queryset(api_client, orders_factory):
    url = reverse('product-list')
    orders = orders_factory(_quantity=5)
    resp = api_client.get(url)
    resp = resp.json()
    print(resp)
    assert resp['results']