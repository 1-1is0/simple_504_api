import csv
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from lesson.models import CourseModel, UnitModel, WordModel
# from my_ap.models import MyModel



class Command(BaseCommand):
    help = 'Command to update some field'
    def add_arguments(self, parser):
        pass
        # parser.add_argument('ids', nargs='+', type=int)

    def handle(self, *args, **options):
        words_csv_file = 'utils/sample_data/words.csv'
        words_csv_file = Path(settings.BASE_DIR, words_csv_file)
        print(words_csv_file)
        course, created = CourseModel.objects.get_or_create(name='504 Absolutely Essential Words') 
        with open(words_csv_file, 'r') as file:
            # reader = csv.reader(file)
            reader = csv.DictReader(file)

            for row in reader:
                unit_id = row['unit']
                unit, created = UnitModel.objects.get_or_create(pk=unit_id, course=course)
                print("row.keys", row.keys())
                examples = f"{row['example_a']}\n{row['example_b']}\n{row['example_c']}"
                word, created = WordModel.objects.get_or_create(
                    unit=unit,
                    word=row['word'],
                    definition=row['definition'],
                    examples=examples
                )
                print("word", word, 'created', created)
