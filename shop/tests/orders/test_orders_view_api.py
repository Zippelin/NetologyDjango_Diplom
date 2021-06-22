import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED


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
    proudcts = products_factory(_quantity=2)
    product_payload = {

        "author": user.id,
        "status": "NEW",
        "total_sum": 22.0,
        "position": [{
            "quantity": 1,
            "product": {
                "id": proudcts[0].id,
                "name": proudcts[0].name,
                "description": proudcts[0].description,
                "price": proudcts[0].price
        }
        }],
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, product_payload, format='json')
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





