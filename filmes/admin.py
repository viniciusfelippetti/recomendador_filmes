from django.contrib import admin

from filmes.models import Filme, Avaliacao

# Register your models here.
admin.site.register(Filme)
admin.site.register(Avaliacao)