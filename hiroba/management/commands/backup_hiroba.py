
import csv
import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Hiroba


class Command(BaseCommand):
    help = "Backup Hiroba data"

    def handle(self, *args, **options):
        date = datetime.date.today().strftime("%Y%m%d")
        file_path = settings.BACKUP_PATH + 'hiroba_' + date + '.csv'

        os.makedirs(settings.BACKUP_PATH, exist_ok=True)
        with open(file_path, "w") as file:
            writer = csv.writer(file)

            header = [field.name for field in Hiroba._meta.fields]
            writer.writerow(header)

            diaries = Hiroba.objects.all()

            for hiroba in diaries:
                writer.writerow([str(hiroba.user),
                                hiroba.title,
                                hiroba.content,
                                str(hiroba.photo),
                                str(hiroba.created_at),
                                str(hiroba.updated_at)])
            files = os.listdir(settings.BACKUP_PATH)
            if len(files) >= settings.NUM_SAVED_BACKUP:
                files.sort()
                os.remove(settings.BACKUP_PATH + files[0])


