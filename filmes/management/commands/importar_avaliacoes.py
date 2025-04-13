from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from filmes.models import Filme, Avaliacao
import csv
import os
from django.conf import settings
from datetime import datetime
from django.utils import timezone

class Command(BaseCommand):
    help = 'Importa avaliações de um arquivo CSV (userId,movieId,rating,timestamp) localizado em filmes/fixtures/ratings.csv e cria os 10 primeiros usuários.'

    def handle(self, *args, **options):
        csv_file_path = os.path.join(settings.BASE_DIR, 'filmes', 'fixtures', 'ratings.csv')

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                imported_count = 0

                for row in reader:
                    user_id = int(row['userId'])
                    movie_id = int(row['movieId'])
                    rating = float(row['rating'])

                    if user_id > 10:
                        self.stdout.write(self.style.SUCCESS('Importação de avaliações finalizada após o userId 10.'))
                        break

                    # Criar usuário se não existir
                    try:
                        usuario = User.objects.get(id=user_id)
                    except User.DoesNotExist:
                        username = f'user{user_id}'
                        email = f'user{user_id}@example.com'  # Você pode ajustar isso
                        usuario = User.objects.create_user(username=username, email=email)
                        self.stdout.write(self.style.SUCCESS(f'Usuário "{username}" criado.'))

                    try:
                        filme = Filme.objects.get(pk=movie_id)
                    except Filme.DoesNotExist:
                        self.stderr.write(self.style.ERROR(f'Filme com ID {movie_id} não encontrado. Avaliação ignorada.'))
                        continue

                    Avaliacao.objects.create(
                        usuario=usuario,
                        filme=filme,
                        nota=rating
                    )
                    imported_count += 1

                self.stdout.write(self.style.SUCCESS(f'{imported_count} avaliações importadas com sucesso.'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'Arquivo CSV não encontrado: "{csv_file_path}"'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ocorreu um erro durante a importação: {e}'))