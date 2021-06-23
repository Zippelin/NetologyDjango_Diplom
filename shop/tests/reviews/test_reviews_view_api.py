import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (False, HTTP_201_CREATED),
        (None, HTTP_401_UNAUTHORIZED),
    )
)
@pytest.mark.django_db
def test_add_review(api_client, user_factory, products_factory, token_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    products = products_factory(_quantity=2)

    payload = {
        "author": user.id,
        "product": products[0].id,
        "text": "test",
        "rating": 1
    }

    url = reverse('review-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (False, HTTP_400_BAD_REQUEST),
    )
)
@pytest.mark.django_db
def test_add_same_review(api_client, user_factory, products_factory, token_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    token = token_factory(user=user)
    products = products_factory(_quantity=2)

    payload = {
        "author": user.id,
        "product": products[0].id,
        "text": "test",
        "rating": 1
    }

    url = reverse('review-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == HTTP_201_CREATED
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_superuser", "http_response"],
    (
        (False, HTTP_405_METHOD_NOT_ALLOWED),
    )
)
@pytest.mark.django_db
def test_update_other_review(api_client, user_factory, products_factory, token_factory, is_superuser, http_response):
    user = user_factory(is_superuser=is_superuser)
    dummy_user = user_factory(is_superuser=True)

    token = token_factory(user=user)
    dummy_token = token_factory(user=dummy_user)

    products = products_factory(_quantity=2)

    payload = {
        "author": dummy_user.id,
        "product": products[0].id,
        "text": "test",
        "rating": 1
    }

    url = reverse('review-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == HTTP_201_CREATED

    payload = {
        "author": dummy_user.id,
        "product": products[0].id,
        "text": "test1",
        "rating": 1
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + dummy_token)
    resp = api_client.put(url, payload, format='json')
    assert resp.status_code == http_response