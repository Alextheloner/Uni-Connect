from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = (
        'Send a real test email to verify your SMTP configuration works, '
        'independent of the password-reset web flow. Usage:\n'
        '  python manage.py send_test_email you@example.com'
    )

    def add_arguments(self, parser):
        parser.add_argument('recipient', type=str, help='Email address to send the test message to')

    def handle(self, *args, **options):
        recipient = options['recipient']

        self.stdout.write(f'EMAIL_BACKEND : {settings.EMAIL_BACKEND}')
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
            self.stdout.write(f'EMAIL_HOST    : {settings.EMAIL_HOST}')
            self.stdout.write(f'EMAIL_PORT    : {settings.EMAIL_PORT}')
            self.stdout.write(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER or "(not set)"}')
            self.stdout.write(f'EMAIL_USE_TLS : {settings.EMAIL_USE_TLS}')
        elif settings.EMAIL_BACKEND == 'django.core.mail.backends.filebased.EmailBackend':
            self.stdout.write(self.style.WARNING(
                'Currently using the FILE-BASED backend (writes to sent_emails/) — '
                'no real email will be delivered. Set EMAIL_HOST_USER and '
                'EMAIL_HOST_PASSWORD (see .env.example) to send real emails instead.'
            ))
        elif settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
            self.stdout.write(self.style.WARNING(
                'Currently using the CONSOLE backend — the message will only be '
                'printed below, not actually delivered. Set EMAIL_HOST_USER and '
                'EMAIL_HOST_PASSWORD (see .env.example) to send real emails instead.'
            ))

        self.stdout.write(f'\nSending test email to {recipient} ...')
        try:
            sent = send_mail(
                subject='Uni-Connect test email',
                message=(
                    'This is a test message from Uni-Connect to confirm that '
                    'outgoing email is configured correctly. If you received '
                    'this, real emails (including password-reset codes) will '
                    'reach your inbox.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
        except Exception as exc:
            raise CommandError(
                f'Failed to send test email: {exc}\n\n'
                'Common causes:\n'
                '  - EMAIL_HOST_USER / EMAIL_HOST_PASSWORD are wrong or missing\n'
                '  - Using your normal account password instead of an App Password (Gmail requires this)\n'
                '  - The SMTP port/TLS settings do not match your provider\n'
                '  - A firewall is blocking outbound SMTP traffic\n\n'
                'See .env.example for setup instructions.'
            )

        if sent:
            self.stdout.write(self.style.SUCCESS(
                f'Success — {sent} message sent to {recipient}. Check the inbox (and spam folder).'
            ))
        else:
            self.stdout.write(self.style.ERROR(
                'The mail backend reported that no message was sent. Check your configuration.'
            ))
