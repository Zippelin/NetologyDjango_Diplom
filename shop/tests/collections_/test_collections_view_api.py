import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (None, HTTP_200_OK),
    )
)
@pytest.mark.django_db
def test_collections_list(api_client, user_factory, token_factory, is_superuser, http_response):
    url = reverse('collection-list')
    resp = api_client.get(url)
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (True, HTTP_201_CREATED),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_post_collections(api_client, user_factory, token_factory, products_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    url = reverse('collection-list')

    products = products_factory(_quantity=1)

    payload = {
        "title": "test",
        "text": "test test",
        "products": [
            {
                "id": products[0].id,
                "name": products[0].name,
                "description": products[0].description,
                "price": products[0].price
            }
        ]
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (True, HTTP_200_OK),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_update_collections(api_client, user_factory, token_factory, collections_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    collection = collections_factory(_quantity=1)

    url = reverse('collection-detail', args=[collection[0].id])

    payload = {
        "id": collection[0].id,
        "title": "test",
        "text": "test test",
        "products": [
            {
                "id": collection[0].products.first().id,
                "name": collection[0].products.first().name,
                "description": collection[0].products.first().description,
                "price": collection[0].products.first().price
            }
        ]
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.put(url, payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (True, HTTP_204_NO_CONTENT),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_delete_collections(api_client, user_factory, token_factory, collections_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    collection = collections_factory(_quantity=1)

    url = reverse('collection-detail', args=[collection[0].id])

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.delete(url)
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["search_field", "search_text", "http_response"],
    (
        ("title", "test_title", HTTP_200_OK),
    )
)
@pytest.mark.django_db
def test_filters_collections(api_client, user_factory, token_factory, collections_factory, search_field, search_text, http_response):
    keys = {
        search_field: search_text
    }
    collection = collections_factory(_quantity=1, **keys)

    url = reverse('collection-list')
    resp = api_client.get(url, params={search_field:search_text})
    assert resp.status_code == http_response
    assert len(resp.json()) == 1

