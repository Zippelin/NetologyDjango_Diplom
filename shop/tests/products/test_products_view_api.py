import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_products_list(api_client):
    url = reverse('product-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (True, HTTP_201_CREATED),
        (False, HTTP_403_FORBIDDEN)
    )
)
@pytest.mark.django_db
def test_product_post(api_client, products_factory, user_factory, token_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    url = reverse('product-list')
    product_payload = {
        "name": "test",
        "description": "text",
        "price": "11.0"
    }

    token = token_factory(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, product_payload, format='json')
    assert resp.status_code == http_response






