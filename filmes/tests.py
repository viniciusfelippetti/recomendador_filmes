import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from filmes.models import Filme, Avaliacao, Genero
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(username='adminuser', password='adminpassword')

@pytest.fixture
def filme1():
    return Filme.objects.create(titulo='Filme 1', sinopse='Sinopse do filme 1')

@pytest.fixture
def filme2():
    return Filme.objects.create(titulo='Filme 2', sinopse='Sinopse do filme 2')

@pytest.fixture
def genero_acao():
    return Genero.objects.create(nome='Ação')

@pytest.fixture
def genero_comedia():
    return Genero.objects.create(nome='Comédia')

@pytest.fixture
def filme_acao(genero_acao):
    filme = Filme.objects.create(titulo='Filme Ação', sinopse='Filme de ação')
    filme.generos.add(genero_acao)
    return filme

@pytest.fixture
def filme_comedia(genero_comedia):
    filme = Filme.objects.create(titulo='Filme Comédia', sinopse='Filme de comédia')
    filme.generos.add(genero_comedia)
    return filme

@pytest.fixture
def avaliacao1(user, filme1):
    return Avaliacao.objects.create(usuario=user, filme=filme1, nota=4)

@pytest.fixture
def avaliacao2(user, filme2):
    return Avaliacao.objects.create(usuario=user, filme=filme2, nota=5)

@pytest.mark.django_db
def test_filme_list_unauthenticated(api_client, filme1, filme2):
    url = reverse('filme-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['titulo'] == filme1.titulo
    assert response.data['results'][1]['titulo'] == filme2.titulo

@pytest.mark.django_db
def test_filme_list_authenticated(api_client, user, filme1, filme2):
    api_client.force_authenticate(user=user)
    url = reverse('filme-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['titulo'] == filme1.titulo
    assert response.data['results'][1]['titulo'] == filme2.titulo

@pytest.mark.django_db
def test_recomendacoes_usuario_authenticated_no_recommendations(api_client, user, filme_acao):
    api_client.force_authenticate(user=user)
    Avaliacao.objects.create(usuario=user, filme=filme_acao, nota=5)
    url = reverse('recomendacoes-usuario', kwargs={'usuario_id': user.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == "Não foram encontradas recomendações para este usuário."

@pytest.mark.django_db
def test_recomendacoes_usuario_unauthenticated(api_client, filme_acao):
    url = reverse('recomendacoes-usuario', kwargs={'usuario_id': 1})
    response = api_client.get(url)
    assert response.status_code == 403
    assert response.data['detail'] == 'Authentication credentials were not provided.'

@pytest.mark.django_db
def test_recomendacoes_usuario_invalid_user(api_client, user, filme_acao):
    api_client.force_authenticate(user=user)
    url = reverse('recomendacoes-usuario', kwargs={'usuario_id': 999})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == "Não foram encontradas recomendações para este usuário."

@pytest.mark.django_db
def test_avaliacao_create_authenticated(api_client, user, filme1):
    api_client.force_authenticate(user=user)
    url = reverse('avaliacao-create')
    data = {'filme': filme1.id, 'nota': 4}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Avaliacao.objects.filter(usuario=user, filme=filme1).exists()
    avaliacao = Avaliacao.objects.get(usuario=user, filme=filme1)
    assert avaliacao.nota == 4

@pytest.mark.django_db
def test_avaliacao_create_unauthenticated(api_client, filme1):
    url = reverse('avaliacao-create')
    data = {'filme': filme1.id, 'nota': 4}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 403
    assert response.data['detail'] == 'Authentication credentials were not provided.'
    assert not Avaliacao.objects.filter(filme=filme1).exists()

@pytest.mark.django_db
def test_avaliacao_create_invalid_filme(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('avaliacao-create')
    data = {'filme': 999, 'nota': 5, 'comentario': 'Incrível!'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'filme' in response.data
    assert response.data['filme'] == [ErrorDetail(string='Invalid pk "999" - object does not exist.', code='does_not_exist')]

@pytest.mark.django_db
def test_avaliacao_create_already_evaluated(api_client, user, filme1):
    api_client.force_authenticate(user=user)
    Avaliacao.objects.create(usuario=user, filme=filme1, nota=3)
    url = reverse('avaliacao-create')
    data = {'filme': filme1.id, 'nota': 4}
    response = api_client.post(url, data, format='json')
    print(Avaliacao.objects.filter(usuario=user, filme=filme1))
    print(response.data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'non_field_errors' in response.data
    assert response.data['non_field_errors'] == [ErrorDetail(string='The fields usuario, filme must make a unique set.', code='unique')]

@pytest.mark.django_db
def test_avaliacao_usuario_list_authenticated(api_client, user, filme1):
    api_client.force_authenticate(user=user)
    Avaliacao.objects.create(usuario=user, filme=filme1, nota=3)
    url = reverse('usuario-avaliacoes', kwargs={'usuario_id': user.id})
    response = api_client.get(url)
    print(Avaliacao.objects.filter(usuario=user))
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['nota'] == 3
    assert response.data['results'][0]['filme_titulo'] == filme1.titulo

@pytest.mark.django_db
def test_avaliacao_usuario_list_unauthenticated(api_client, user):
    url = reverse('usuario-avaliacoes', kwargs={'usuario_id': user.id})
    response = api_client.get(url)
    assert response.status_code == 403
    assert response.data['detail'] == 'Authentication credentials were not provided.'

@pytest.mark.django_db
def test_avaliacao_usuario_list_invalid_user(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('usuario-avaliacoes', kwargs={'usuario_id': 999})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND