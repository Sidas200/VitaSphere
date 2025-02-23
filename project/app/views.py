from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import RegistroUsuarioForm
from django.contrib.auth.hashers import make_password
from bson.objectid import ObjectId 
from django.contrib.auth.hashers import check_password
from .models import person_collection

def apps(request):
    return HttpResponse("Hello world!")

def primero(request):
    nombre = "Pedro"
    apellido = "Sanchez"
    return render(request, 'primero.html', {"nombre":nombre, "apellido":apellido})


def registro_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            apellidos = form.cleaned_data["apellidos"]
            telefono = form.cleaned_data["telefono"]
            domicilio = form.cleaned_data["domicilio"]
            estatus = form.cleaned_data["status"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            fecha = form.cleaned_data["fecha"]

            existing_user = person_collection.find_one({"username": username})
            if existing_user:
                return HttpResponse("El usuario ya existe", status=400)

            hashed_password = make_password(password)

        
            person_collection.insert_one({
                "_id": ObjectId(),
                "nombre": name,
                "apellidos": apellidos,
                "telefono": telefono,
                "domicilio": domicilio,
                "estatus": estatus,
                "username": username,
                "email": email,
                "password": hashed_password,
                "fecha":fecha
            })

            return redirect("login")

    else:
        form = RegistroUsuarioForm()

    return render(request, "registro.html", {"form": form})

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return HttpResponse("Por favor, ingresa usuario y contraseña", status=400)

        user = person_collection.find_one({"email": email})

        if user and check_password(password, user["password"]):
            request.session["username"] = user["username"]
            request.session["email"] = user["email"]
            request.session["nombre"] = user["nombre"]
            request.session["is_authenticated"] = True
    
            return redirect("users")

        return HttpResponse("Usuario o contraseña incorrectos", status=401)

    return render(request, "login.html")

def logout_view(request):
    request.session.flush()
    return redirect("login")

def users(request):
    if not request.session.get("is_authenticated", False):
        return redirect("login")

    user_list = person_collection.find({}, {"_id": 0, "username": 1, "email": 1})

    return render(request, "users.html", {"users": user_list})

def home (request):
    return render(request, "home.html")

def datos(request):
    return render(request, "datos.html")

def profile (request):
    return render(request, "profile.html")


