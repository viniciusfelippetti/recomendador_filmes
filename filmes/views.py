from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from filmes.models import Filme, Avaliacao
from filmes.serializers import FilmeSerializerWithoutDetails, AvaliacaoSerializer, AvaliacaoUsuarioSerializer


class FilmeList(generics.ListAPIView):
    """
    Lista todos os filmes disponíveis (não necessita de autenticação).
    """
    queryset = Filme.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = FilmeSerializerWithoutDetails
    permission_classes = [IsAuthenticatedOrReadOnly]

class RecomendacoesUsuario(generics.ListAPIView):
    """
    Retorna recomendações personalizadas para um usuário específico (com paginação e necessita de autenticação).
    """
    serializer_class = FilmeSerializerWithoutDetails
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        usuario_id = self.kwargs.get('usuario_id')
        try:
            usuario = User.objects.get(id=usuario_id)
        except User.DoesNotExist:
            return Filme.objects.none()

        # Buscar as avaliações dos 5 filmes com as maiores notas do usuário (retorna os generos do filme)
        top_avaliacoes_usuario = Avaliacao.objects.filter(usuario=usuario) \
                                     .order_by('-nota') \
                                     .values_list('filme__generos__nome', flat=True) \
                                     .distinct()[:5]

        # Busca filmes que pertencem a esses gêneros (excluindo os já avaliados pelo usuário)
        filmes_recomendados = Filme.objects.filter(generos__nome__in=top_avaliacoes_usuario) \
            .exclude(avaliacao__usuario=usuario) \
            .distinct()

        # Ordenação pela melhor média de avaliações dos filmes recomendados
        filmes_recomendados = filmes_recomendados.annotate(avg_nota_geral=Avg('avaliacao__nota'))
        filmes_recomendados = filmes_recomendados.order_by('-avg_nota_geral')

        return filmes_recomendados[:40]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Não foram encontradas recomendações para este usuário."},
                            status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)

class AvaliacaoCreate(generics.CreateAPIView):
    """
    Permite que usuários autenticados avaliem um filme.
    """
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        filme_id = self.request.data.get('filme')
        try:
            filme = Filme.objects.get(pk=filme_id)
        except Filme.DoesNotExist:
            raise serializers.ValidationError({"filme": "Filme não encontrado."})

        if Avaliacao.objects.filter(usuario=self.request.user, filme=filme).exists():
            raise serializers.ValidationError({"detail": "Você já avaliou este filme."})

        serializer.save(usuario=self.request.user, filme=filme)


class AvaliacaoUsuarioList(generics.ListAPIView):
    """
    Lista as avaliações de um usuário específico, mostrando filme e nota.
    Ordenado por notas mais altas.
    """
    serializer_class = AvaliacaoUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario_id = self.kwargs.get('usuario_id')
        usuario = get_object_or_404(User, id=usuario_id)
        return Avaliacao.objects.filter(usuario=usuario).select_related('filme').order_by('-nota')