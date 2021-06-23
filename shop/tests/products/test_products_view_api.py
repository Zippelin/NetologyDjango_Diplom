import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT, \
    HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_products_list(api_client):
    url = reverse('product-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (True, HTTP_200_OK),
        (False, HTTP_200_OK)
    )
)
@pytest.mark.django_db
def test_products_details(api_client, products_factory, user_factory, token_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    products = products_factory(_quantity=1)
    url = reverse('product-detail', args=[products[0].id])
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url)
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (True, HTTP_201_CREATED),
        (False, HTTP_403_FORBIDDEN)
    )
)
@pytest.mark.django_db
def test_post_product(api_client, products_factory, user_factory, token_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    url = reverse('product-list')
    product_payload = {
        "name": "test",
        "description": "text",
        "price": "11.0"
    }


    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, product_payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (True, HTTP_201_CREATED),
        (False, HTTP_403_FORBIDDEN)
    )
)
@pytest.mark.django_db
def test_update_product(api_client, products_factory, user_factory, token_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    url = reverse('product-list')
    product_payload = {
        "name": "test",
        "description": "text",
        "price": "11.0"
    }


    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, product_payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (True, HTTP_204_NO_CONTENT),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_delete_product(api_client, user_factory, token_factory, products_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    product = products_factory(_quantity=1)
    url = reverse('product-detail', args=[product[0].id])

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.delete(url)
    assert resp.status_code == http_response



@pytest.mark.parametrize(
    ["search_field", "search_text", "http_response"],
    (
        ("name", "test_name", HTTP_200_OK),
        ("price", "10", HTTP_200_OK),
        ("description", "test_description", HTTP_200_OK),
    )
)
@pytest.mark.django_db
def test_filters_products(api_client, products_factory, search_field, search_text, http_response):
    keys = {
        search_field: search_text
    }
    _ = products_factory(_quantity=1, **keys)

    url = "%s?%s=%s" % (reverse('product-list'), search_field, search_text)
    resp = api_client.get(url)
    assert resp.status_code == http_response
    assert len(resp.json()) == 1




