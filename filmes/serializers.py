from django.contrib.auth.models import User
from rest_framework import serializers

from filmes.models import Filme, Avaliacao


class FilmeSerializerWithoutDetails(serializers.ModelSerializer):
    generos = serializers.SlugRelatedField(many=True, read_only=True, slug_field='nome')

    class Meta:
        model = Filme
        fields = ['id', 'titulo', 'generos']

class FilmeSerializer(FilmeSerializerWithoutDetails):
    diretor = serializers.SlugRelatedField(read_only=True, slug_field='nome')
    atores = serializers.SlugRelatedField(many=True, read_only=True, slug_field='nome')
    class Meta(FilmeSerializerWithoutDetails.Meta):
        fields = FilmeSerializerWithoutDetails.Meta.fields + ['sinopse', 'ano_lancamento', 'diretor', 'atores']

class AvaliacaoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    filme = serializers.PrimaryKeyRelatedField(queryset=Filme.objects.all())

    class Meta:
        model = Avaliacao
        fields = ['id', 'usuario', 'filme', 'nota', 'data_avaliacao']
        read_only_fields = ['data_avaliacao']

class AvaliacaoUsuarioSerializer(serializers.ModelSerializer):
    filme_titulo = serializers.CharField(source='filme.titulo', read_only=True)

    class Meta:
        model = Avaliacao
        fields = ['filme_titulo', 'nota', 'data_avaliacao']