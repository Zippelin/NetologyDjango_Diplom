import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_products_list(api_client):
    url = reverse('product-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_product_post(api_client, products_factory):
    user_admin = get_user_model().objects.create(username="admin", password="admin", email="admin@admin.com", is_superuser=True, is_staff=True)
    simple_user = get_user_model().objects.create(username="user", password="user", email="user@user.com")
    url = reverse('product-list')
    product_payload = {
        "name": "test",
        "description": "text",
        "price": "11.0"
    }
    api_client.force_authenticate(user_admin)
    resp = api_client.post(url, product_payload, format='json')
    assert resp.status_code == HTTP_201_CREATED

    api_client.force_authenticate(simple_user)
    resp = api_client.post(url, product_payload, format='json')
    print(resp.status_code)
    assert resp.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_product_post(api_client, products_factory):
    user_admin = get_user_model().objects.create(username="admin", password="admin", email="admin@admin.com",
                                                 is_superuser=True, is_staff=True)
    simple_user = get_user_model().objects.create(username="user", password="user", email="user@user.com")
    url = reverse('product-list')
    product_payload = {
        "id": 1,
        "name": "test",
        "description": "text",
        "price": "11.0"
    }
    api_client.force_authenticate(user_admin)
    resp = api_client.patch(url, product_payload, format='json')
    assert resp.status_code == HTTP_201_CREATED

    url = reverse('product-detail')
    product_payload = {

        "name": "test",
        "description": "text",
        "price": "11.0"
    }

    resp = api_client.patch(url, product_payload, format='json')
    assert resp.status_code == HTTP_201_CREATED





