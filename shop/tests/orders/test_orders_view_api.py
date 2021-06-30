import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (True, HTTP_200_OK),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_orders_list(api_client, user_factory, token_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    url = reverse('order-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
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
def test_post_orders(api_client, user_factory, token_factory, products_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    url = reverse('order-list')
    products = products_factory(_quantity=2)
    product_payload = {

        "author": user.id,
        "status": "NEW",
        "position": [{
            "quantity": 1,
            "product": products[0].id
        }],
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, product_payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (True, HTTP_200_OK),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_update_orders(api_client, user_factory, token_factory, orders_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    orders = orders_factory(_quantity=1)
    url = reverse('order-detail', args=[orders[0].id])
    product_payload = {
        "status": "NEW",
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.put(url, product_payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (True, HTTP_204_NO_CONTENT),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_delete_orders(api_client, user_factory, token_factory, orders_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    orders = orders_factory(_quantity=1)
    url = reverse('order-detail', args=[orders[0].id])

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.delete(url)
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_superuser",],
    (
        (True,),
        (False,)
    )
)
@pytest.mark.django_db
def test_unique_per_user_orders(api_client, user_factory, token_factory, orders_factory, is_superuser):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    url = reverse('order-list')
    orders = orders_factory(_quantity=10)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url)
    print(resp)
    if is_superuser:
        assert len(resp.json()) == 10
    else:
        assert len(resp.json()) < 10


@pytest.mark.parametrize(
    ["search_field", "search_text", "http_response"],
    (
            ("status", "NEW", HTTP_200_OK),
            ("total_sum", "10", HTTP_200_OK),
            ("date_creation", '2021-06-23', HTTP_200_OK),
            ("date_update", '2021-06-23', HTTP_200_OK),
            ("products", None, HTTP_200_OK),
    )
)
@pytest.mark.django_db
def test_filters_orders(api_client, user_factory, token_factory, orders_factory, search_field, search_text,
                          http_response):

    user = user_factory(is_superuser=True)
    token = token_factory(user=user)
    if search_text is not None:
        keys = {
            search_field: search_text
        }
        orders = orders_factory(_quantity=1, **keys)
    else:
        orders = orders_factory(_quantity=1)
        search_text = orders[0].products.first().id
    url = reverse('order-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url, params={search_field:search_text})
    assert resp.status_code == http_response
    assert len(resp.json()) == 1


