import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from recipes.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'load ingredients'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='ingredients.json', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        with open(os.path.join(DATA_ROOT, options['filename']), 'r',
                  encoding='utf-8') as f:
            data = json.load(f)
            for ingredient in data:
                try:
                    Ingredient.objects.create(name=ingredient["name"],
                                              measurement_unit=ingredient[
                                              "measurement_unit"])
                except IntegrityError:
                    print(f'Ингредиент {ingredient["name"]} '
                          f'{ingredient["measurement_unit"]} '
                          f'есть в базе')
