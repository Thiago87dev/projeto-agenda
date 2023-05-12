from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato

def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'usuario e/ou senha incorreto(s)')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, f'{request.POST.get("usuario")} logado com sucesso')
        return redirect('index')
    
def logout(request):
    auth.logout(request)
    return redirect('login') 
    
def cadastro(request):
    if request.method !='POST':
        return render(request, 'accounts/cadastro.html')
    
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not email or not usuario or not nome or not sobrenome or not senha or not senha2:
        messages.error(request, 'Nenhum campo pode ficar vazio')
        return render(request, 'accounts/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email invalido')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 6:
        messages.error(request, 'sua senha deve ter no minimo 6 caracteres')
        return render(request, 'accounts/cadastro.html')

    if len(usuario) < 6:
        messages.error(request, 'usuario deve ter no minimo 6 caracteres')
        return render(request, 'accounts/cadastro.html')

    if senha != senha2:
        messages.error(request, 'As senhas não conferem')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Este usuario ja existe')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Este email ja esta cadastrado')

    messages.success(request, 'Registrado com sucesso, agora vc pode fazer login')
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()
    return redirect('login')
    
@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'erro ao salvar formulario')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'contato {request.POST.get("nome")} salvo com sucesso')
    return redirect('dashboard')
