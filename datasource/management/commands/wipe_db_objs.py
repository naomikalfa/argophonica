from datasource.models import Album, Artist, Track
from django.core.management.base import BaseCommand
import sys


class Command(BaseCommand):

    def handle(self, *args, **options):

        def yes_check():
            print(f"Warning! This will delete all data in the database, type YES in capitals to continue")
            answer = input()
            if answer == 'YES':
                return answer
            else:
                print('Aborted')
                sys.exit()

        answer = yes_check()

        if answer == 'YES':

            print("\nSo you have chosen ... DEATH!"
                  "\nData death!\n"
                  "\nModels:\n"
                  " ALBUM\n"
                  " ARTIST\n"
                  " TRACK\n"
                  " ALL\n"
                  "\nChoose the model you want to DROP <- !warning!\n"
                  "Type it in capitals to continue\n")
            model_type = input()

            if model_type == 'ALBUM':
                Album.objects.all().delete()
                print('Data from', model_type, 'cleared')

            elif model_type == 'ARTIST':
                Artist.objects.all().delete()
                print('Data from', model_type, 'cleared')

            elif model_type == 'TRACK':
                Track.objects.all().delete()
                print('Data from', model_type, 'cleared')

            elif model_type == 'ALL':
                Track.objects.all().delete()
                Artist.objects.all().delete()
                Album.objects.all().delete()
                print('Data from', model_type, 'cleared')

            else:
                print('Aborted')

        else:
            print('Aborted')
