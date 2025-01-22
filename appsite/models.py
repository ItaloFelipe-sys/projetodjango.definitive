from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField('Título', max_length=200)
    texto = models.TextField('Mensagem')
    imagem = models.ImageField('Imagem', upload_to='posts/', null=True, blank=True)
    contato = models.CharField('Contato', max_length=100, default='')
    data_criacao = models.DateTimeField(default=timezone.now)
    data_publicacao = models.DateTimeField(blank=True, null=True)

    def publicar(self):
        self.data_publicacao = timezone.now()
        self.save()

    def __str__(self):
        return self.titulo

class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField('Sobre mim', max_length=500, blank=True)
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True)