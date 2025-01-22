from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Perfil

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo', 'texto', 'imagem', 'contato')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input'}),
            'texto': forms.Textarea(attrs={'class': 'form-textarea'}),
            'contato': forms.TextInput(attrs={'class': 'form-input'}),
            'imagem': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'id_imagem_input'})
        }

class CadastroForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('bio', 'telefone', 'cidade')
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Opcional'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Opcional'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Opcional'
            })
        }
        labels = {
            'bio': 'Sobre mim (opcional)',
            'telefone': 'Telefone (opcional)',
            'cidade': 'Cidade (opcional)'
        }