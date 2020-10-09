from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core import validators
import uuid
import re
from core.api.v1.models.indexed_file import Location, HealthInsurance
from django.contrib.auth.hashers import identify_hasher


class UserModel(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, verbose_name=_('uuid'), default=uuid.uuid4,
                          editable=False, unique=True)
    username = models.CharField(
        'Nome de usuário', max_length=30, unique=True, validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'Informe um nome de usuário válido. '
                'Este valor deve conter apenas letras, números '
                'e os caracteres: @/./+/-/_ .'
                , 'invalid'
            )
        ], help_text='Um nome curto que será usado para identificá-lo de forma única na plataforma'
    )
    nickname = models.CharField("Com quer ser chamado", max_length=255, null=True)
    email = models.EmailField('E-mail', unique=True, null=True, blank=True)
    password = models.CharField("Senha", max_length=255)
    is_staff = models.BooleanField('Time', default=False)
    is_active = models.BooleanField('Usuário Ativo', default=True)
    is_superuser = models.BooleanField('Super Usuário', default=False)
    date_joined = models.DateTimeField('Criado em:', auto_now_add=True)
    last_update = models.DateTimeField('Atualizado em:', auto_now=True)

    locations = models.ManyToManyField(Location, related_name='users', blank=True)
    health_insurances = models.ManyToManyField(HealthInsurance, related_name='users', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return str(self)

    def date_published(self):
        return self.date_joined.strftime('%B %d %Y')

    def get_short_name(self):
        return str(self).split(" ")[0]

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.password)
        except ValueError:
            self.set_password(self.password)
        super(UserModel, self).save(*args, **kwargs)
