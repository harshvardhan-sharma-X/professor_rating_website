# filepath: d:\vit_website\vit_website\professors\management\commands\load_professors.py
from django.core.management.base import BaseCommand, CommandError
from professors.models import Professor
import json

class Command(BaseCommand):
    help = 'Loads professor data from a JSON file into the database.'

    def handle(self, *args, **options):
        try:
            with open('professors/data.json', 'r') as f:
                data = json.load(f)

                for item in data:
                    if item['model'] == 'professors.professor':
                        try:
                            Professor.objects.create(name=item['fields']['name'])
                            self.stdout.write(self.style.SUCCESS(f"Successfully created professor: {item['fields']['name']}"))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"Error creating professor {item['fields']['name']}: {e}"))

            self.stdout.write(self.style.SUCCESS('Successfully loaded professor data.'))

        except FileNotFoundError:
            raise CommandError('data.json file not found in the professors directory.')
        except json.JSONDecodeError:
            raise CommandError('Invalid JSON format in data.json.')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')