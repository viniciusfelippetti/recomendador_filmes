from django.contrib.auth.models import User
from django.db import models


class Genero(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Diretor(models.Model):
    nome = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome


class Ator(models.Model):
    nome = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome


class Filme(models.Model):
    titulo = models.CharField(max_length=255)
    generos = models.ManyToManyField(Genero, related_name='generos')
    diretor = models.ForeignKey(Diretor, on_delete=models.SET_NULL, null=True, blank=True)
    atores = models.ManyToManyField(Ator, blank=True)
    sinopse = models.TextField(blank=True)
    ano_lancamento = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.titulo} - {self.ano_lancamento}'

class Avaliacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
    nota = models.FloatField(null=True, blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'filme')

    def __str__(self):
        return f"Avaliação de {self.usuario.username} para {self.filme.titulo}"