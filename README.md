# API Sistema de Recomendação de Filmes
✅ Projeto desenvolvido com as ferramentas: 
<div style="display: inline_block">
  <img align="center" alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img align="center" alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img align="center" alt="Django" src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img align="center" alt="Django Rest Framework" src="https://img.shields.io/badge/Django_REST_Framework-092E20?style=for-the-badge&logo=django&logoColor=red" />
</div>

## Requisitos

- Python 3.8+
- pip 25.0.1
- Django 5+
- Docker 25+

 ### 1. Git Clone do Projeto
Clone o projeto para sua máquina:
```bash
https://github.com/viniciusfelippetti/recomendador_filmes.git
```

 ### 2. Entre no diretório do projeto
```bash
cd recomendador_filmes/
```

### 3. Rodar Comandos
Cria os containers do banco, do app, e roda todos os comando necessários para início do projeto (instala os requirements, roda o arquivo configuracoes_iniciais, importar_filmes_generos, importar_avaliacoes, realiza todos os testes, o makemigrations, o migrate...)
```bash
docker-compose build
docker-compose up
```
### Arquivo Importar Livros e Generos
A partir do arquivo movies.csv, importa os livros e os generos, e faz a vinculação dos generos ao livro.

### Arquivo Importar Avaliacoes
A partir do arquivo ratings.csv, importa as avaliações até o usuário com id=10, os usuários do id 2 ao 10 são criados(o usuário com id=1, é o admin).

### Arquivo Configurações Iniciais
Cria um usuário padrão com Username 'admin' e senha 'admin123'. Vai ser usado para se autenticar no Swagger e poder testar as Apis.

### Realização dos testes
Roda os testes unitários das APIS.

# APIS


<b>As APIS estão documentadas no Swagger, segue o caminho para acessar a documentação:</b>
```bash
api/swagger
```

