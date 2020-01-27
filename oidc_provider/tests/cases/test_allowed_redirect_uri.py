import pytest
from oidc_provider.tests.app.utils import create_fake_client


@pytest.mark.django_db
@pytest.mark.parametrize("allowed_redirect_uris, redirect_uri, expected", [
    # Exact match
    (
        ["https://user:password@example.com?param=value#fragment"],
        "https://user:password@example.com?param=value#fragment",
        True
    ),
    # Normal fail
    (
        ["https://user:password@example.com?param=value#fragment"],
        "https://user:password@example.com?param=bad#fragment",
        False
    ),
    # Accepts one of list
    (["https://a.com", "https://b.com", "https://c.com"], "https://a.com", True),
    # Port ignored for loopback (v4)
    (["127.0.0.1"], "127.0.0.1:5000", True),
    # Port ignored for loopback (v6)
    (["[::1]"], "[::1]:5000", True),
    # Port specified in config ignored (v6)
    (["[::1]:5000"], "[::1]", True),
    # Configured URI which could not be parsed falls back to others
    (["::]", "[::1]:5000"], "[::1]:3000", True),
    # Localhost not accepted as loopback
    (["localhost"], "localhost:3000", False),
    # Custom URI schemes accepted (exact match)
    (["customscheme://openid/callback"], "customscheme://openid/callback", True),
    # Claimed https (reverse-DNS) accepted
    (["https://com.example.app/callback"], "https://com.example.app/callback", True),
])
def test_redirect_uri(allowed_redirect_uris, redirect_uri, expected):
    client = create_fake_client("code")
    client.redirect_uris = allowed_redirect_uris
    assert client.is_allowed_redirect_uri(redirect_uri) == expected
