# products/management/commands/check_cors.py
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Check current CORS configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== CORS Configuration ==='))
        self.stdout.write(f'CORS_ALLOW_ALL_ORIGINS: {settings.CORS_ALLOW_ALL_ORIGINS}')
        self.stdout.write(f'CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}')
        self.stdout.write(f'CORS_ALLOW_CREDENTIALS: {settings.CORS_ALLOW_CREDENTIALS}')
        self.stdout.write(f'CORS_URLS_REGEX: {settings.CORS_URLS_REGEX}')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== Environment Variables ==='))
        import os
        self.stdout.write(f'CORS_ALLOW_ALL_ORIGINS (env): {os.environ.get("CORS_ALLOW_ALL_ORIGINS", "Not set")}')
        self.stdout.write(f'CORS_ALLOWED_ORIGINS (env): {os.environ.get("CORS_ALLOWED_ORIGINS", "Not set")}')
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('If CORS is not working, check:'))
        self.stdout.write('1. CORS_ALLOWED_ORIGINS includes your frontend domain')
        self.stdout.write('2. CORS middleware is at the top of MIDDLEWARE list')
        self.stdout.write('3. Environment variables are set correctly in docker-compose or .env file')

