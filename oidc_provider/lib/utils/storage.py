from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ImproperlyConfigured

from oidc_provider import settings

location = settings.get('OIDC_RSA_CERT_LOCATION')

if settings.get('OIDC_RSA_CERT_STORE') == 'filesystem' and location is None:
    raise ImproperlyConfigured("OIDC_RSA_CERT_LOCATION must be configured if OIDC_RSA_CERT_STORE='filesystem'")

class KeyStorage(FileSystemStorage):
    location = location
    file_permissions_mode = 0o600
