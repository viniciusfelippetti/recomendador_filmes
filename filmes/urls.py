from django.urls import path
from . import views

urlpatterns = [
    path('filmes/', views.FilmeList.as_view(), name='filme-list'),
    path('filmes/<int:usuario_id>/recomendacoes/', views.RecomendacoesUsuario.as_view(), name='recomendacoes-usuario'),
    path('avaliacoes/', views.AvaliacaoCreate.as_view(), name='avaliacao-create'),
    path('usuarios/<int:usuario_id>/avaliacoes/', views.AvaliacaoUsuarioList.as_view(), name='usuario-avaliacoes'),

]