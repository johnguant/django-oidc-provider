from Cryptodome.PublicKey import RSA
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from django.conf import settings
from oidc_provider.models import RSAKeyDatabase, RSAKeyFilesystem


class Command(BaseCommand):
    help = 'Migrate RSA keys from the database to the filesystem.'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('--copy', help='Copy keys instead of moving them', action='store_true')
        parser.add_argument('--ignore-media-root', help='Migrate even if MEDIA_ROOT is unset', action='store_true')

    def handle(self, *args, **options):
        if settings.MEDIA_ROOT == "" and not options['ignore_media_root']:
            raise CommandError(
                "MEDIA_ROOT not set. You should set this to a writable "
                "directory before running this command, or bypass this warning with --ignore-media-root"
            )

        for key in RSAKeyDatabase.objects.all():
            new = RSAKeyFilesystem()
            new._key.save(key.kid, ContentFile(key.key))
            if not options['copy']:
                key.delete()
            self.stdout.write("{} key with kid: {}".format("Copied" if options['copy'] else "Moved", new.kid))
