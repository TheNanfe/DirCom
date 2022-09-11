from django.core.management.base import BaseCommand

from applications.users.models import Persona


class Command(BaseCommand):
    help = "Crear una persona desde la consola"

    def add_arguments(self, parser):
        parser.add_argument('gov_id', type=str, help='Número de documento de identidad')
        parser.add_argument('email', type=str, help='Email')

    def handle(self, *args, **kwargs):
        gov_id = kwargs['gov_id']
        email = kwargs['email']

        Persona.objects.create(
            gov_id=gov_id,
            email=email,
        )