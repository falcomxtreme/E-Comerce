from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Importação dos modelos
from .models import User, UserContact, UserAddress


# Formulário de registro de usuário, estendendo UserCreationForm para incluir CPF e outros dados
class UserRegisterForm(UserCreationForm):
    cpf = forms.CharField(
        max_length=11,
        required=True,
        label="CPF",
        help_text="Digite o CPF sem pontos ou traços.",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "cpf",
            "password1",
            "password2",
        ]

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError("CPF deve ter 11 dígitos numéricos.")
        if User.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Um usuário com este CPF já existe.")
        return cpf


# Formulário de atualização de dados do usuário
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "cpf"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if cpf and User.objects.exclude(pk=self.instance.pk).filter(cpf=cpf).exists():
            raise forms.ValidationError("Um usuário com este CPF já existe.")
        return cpf


# Formulário de login do usuário
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuário ou E-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("Esta conta está inativa.", code="inactive")


# Formulário de contato do usuário
class UserContactForm(forms.ModelForm):
    class Meta:
        model = UserContact
        fields = ["contact_type", "phone_number", "main_contact"]

    def clean_main_contact(self):
        main_contact = self.cleaned_data.get("main_contact")
        if (
            main_contact
            and UserContact.objects.filter(
                user=self.instance.user, main_contact=True
            ).exists()
        ):
            raise forms.ValidationError("Este usuário já possui um contato principal.")
        return main_contact


# Formulário de endereço do usuário
class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
            "address_type",
            "zip_code",
            "city",
            "state",
            "street",
            "number",
            "complement",
        ]

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get("zip_code")
        if not zip_code.isdigit() or len(zip_code) != 8:
            raise forms.ValidationError("CEP deve ter 8 dígitos numéricos.")
        return zip_code
