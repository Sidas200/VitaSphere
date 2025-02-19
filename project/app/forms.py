from django import forms

class RegistroUsuarioForm(forms.Form):
    name = forms.CharField(label="Nombre de la persona", max_length=20)
    apellidos = forms.CharField(label="Apellido de la persona", max_length=30)
    telefono = forms.CharField(label="Telefono de la persona", max_length=15)
    domicilio = forms.CharField(label="Domicilio de la persona", max_length=100)
    status = forms.BooleanField(label="Estatus de la persona")
    username = forms.CharField(label="Nombre de usuario", max_length=100)
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    fecha = forms.CharField(label="fecha")