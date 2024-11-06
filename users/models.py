from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

from django.utils import timezone


# Modelo de usuário
class User(AbstractUser):
    # Nome de usuário -  Único para cada usuário
    username = models.CharField(max_length=30, unique=True, verbose_name="Usuário")
    # Nome
    first_name = models.CharField(max_length=50, verbose_name="Nome")
    # Sobrenome
    last_name = models.CharField(max_length=50, verbose_name="Sobrenome")
    # Email - Único para cada usuário
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="E-mail",
        error_messages={
            "invalid": "Por favor, insira um endereço de e-mail válido.",
            "required": "O campo de e-mail é obrigatório.",
        },
    )
    cpf = models.CharField(
        max_length=11, unique=True, blank=True, null=True, verbose_name="CPF"
    )
    # Senha
    password = models.CharField(max_length=128, verbose_name="Senha")
    # Data de criação
    created_at = models.DateTimeField(default=timezone.now)
    # Atualizado em
    updated_at = models.DateTimeField(auto_now=True)

    # Método para definir a senha, armazenando-a como hash
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    # Garantia de hash na senha
    def save(self, *args, **kwargs):
        # Caso a senha não esteja criptografada(Hash)
        if not self.password.startswith("pbkdf2_"):
            # Faz o hash da senha
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.email})"


class UserContact(models.Model):
    # Relaciona o modelo de contato com modelo de usuário via ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contatos")
    # Tipo de contato "Email", "WhatsApp", etc.
    contact_type = models.CharField(max_length=50)
    # Telefone para contato
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Telefone"
    )
    # Contato principal?
    main_contact = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo}: {self.valor} ({self.usuario.username})"


# Modelo de Endereço para o Usuário
class UserAddress(models.Model):
    # Relaciona o modelo de endereço com modelo de usuário via ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enderecos")
    # Tipo de endereço
    address_type = models.CharField(
        max_length=20,
        choices=[("residential", "Residencial"), ("commercial", "Comercial")],
    )
    # CEP
    zip_code = models.CharField(max_length=8, verbose_name="CEP")
    # Nome da cidade
    city = models.CharField(max_length=50, verbose_name="Cidade")
    # Sigla do estado
    state = models.CharField(max_length=2, verbose_name="Estado")
    # Nome da Rua
    street = models.CharField(max_length=100, verbose_name="Rua")
    # Número da residência
    number = models.CharField(max_length=10, verbose_name="Número")
    # Complemento opcional
    complement = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Complemento"
    )

    def __str__(self):
        return (
            f"{self.street}, {self.number} - {self.city}/{self.state} ({self.zip_code})"
        )


# TODO Modelo de histórico de pedidos
