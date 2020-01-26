import pytest
from oidc_provider.tests.app.utils import create_fake_client


@pytest.mark.django_db
@pytest.mark.parametrize("allowed_redirect_uris, redirect_uri, expected", [
    (
        ["https://user:password@example.com?param=value#fragment"],
        "https://user:password@example.com?param=value#fragment",
        True
    ),
    (
        ["https://user:password@example.com?param=value#fragment"],
        "https://user:password@example.com?param=bad#fragment",
        False
    ),
    (["https://a.com", "https://b.com", "https://c.com"], "https://a.com", True),
    (["127.0.0.1"], "127.0.0.1:5000", True),
    (["[::1]"], "[::1]:5000", True),
    (["[::1]:5000"], "[::1]", True),
])
def test_redirect_uri(allowed_redirect_uris, redirect_uri, expected):
    client = create_fake_client("code")
    client.redirect_uris = allowed_redirect_uris
    assert client.is_allowed_redirect_uri(redirect_uri) == expected
