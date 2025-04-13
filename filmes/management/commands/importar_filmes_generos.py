# manage.py/commands/import_filmes_generos.py
from django.core.management.base import BaseCommand
from filmes.models import Filme, Genero
import csv
import re
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Importa filmes e gêneros de um arquivo CSV no formato "id,Nome do Filme (Ano),Gênero1|Gênero2|..." localizado em filmes/fixtures/movies.csv'

    def handle(self, *args, **options):
        csv_file_path = os.path.join(settings.BASE_DIR, 'filmes', 'fixtures', 'movies.csv')

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # Pula a primeira linha do cabeçalho, se houver

                for row in reader:
                    if len(row) >= 2:
                        raw_data = row[1]
                        match = re.match(r"(.+)\s\((\d{4})\)", raw_data)
                        if match:
                            titulo = match.group(1).strip()
                            ano_lancamento = int(match.group(2))
                            generos_str = row[2].split('|') if len(row) > 2 else []

                            filme, filme_criado = Filme.objects.get_or_create(
                                titulo=titulo,
                                ano_lancamento=ano_lancamento
                            )

                            for genero_nome in generos_str:
                                genero_nome = genero_nome.strip()
                                if genero_nome:
                                    genero, genero_criado = Genero.objects.get_or_create(nome=genero_nome)
                                    filme.generos.add(genero)

                            self.stdout.write(self.style.SUCCESS(f'Filme "{titulo} ({ano_lancamento})" e seus gêneros importados com sucesso.'))
                        else:
                            self.stderr.write(self.style.ERROR(f'Erro ao processar linha: Formato do filme incorreto: "{raw_data}"'))
                    else:
                        self.stderr.write(self.style.ERROR(f'Erro ao processar linha: Número de colunas insuficiente.'))

            self.stdout.write(self.style.SUCCESS('Importação de filmes e gêneros concluída.'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'Arquivo CSV não encontrado: "{csv_file_path}"'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ocorreu um erro durante a importação: {e}'))