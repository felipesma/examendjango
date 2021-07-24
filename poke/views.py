from django.shortcuts import render, HttpResponse, redirect
from poke.models import *
from django.db.models import Count
from operator import itemgetter
from django.contrib import messages
import bcrypt


# Create your views here.

def index(request):
    return redirect('main/')

def main(request):
    return render(request, 'main.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect ('/main/')

    else:
        if request.method == 'POST':
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(name=request.POST['name'],alias=request.POST['alias'],email=request.POST['email'],password=password,birth_date=request.POST['birth'])
            return redirect('/main/')
        else:
            return redirect('/main/')

def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST["email"])
        if len(user) == 1:
            if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
                request.session['email'] = request.POST["email"]
                return redirect('/pokes/')

def logout(request):
    if request.method == 'GET':
        if request.session.get('email') != None:
            request.session.flush()
            return redirect('/')

def pokes(request): 
    if request.method == 'GET':
        if request.session.get('email') != None:
            email = request.session['email']
            loged = User.objects.get(email = email)
            print('Usuario Logueado:', loged.name)
            users = User.objects.exclude(email=email)
            loged_pokes = []
            for poke in loged.pokes.all():
                loged_pokes.append(poke.origin_user.alias)
            def countPokes(list):
                return {i:list.count(i) for i in list}
            all_pokes = countPokes(loged_pokes)
            pokes = sorted(all_pokes.items(), key=itemgetter(1), reverse=True)
            print('pokes:', pokes)
            context = {
                'loged': loged,
                'users': users,
                'pokes': pokes,
            }
            return render(request, 'pokes.html', context=context)
        else:
            return redirect('/')
    elif request.method == 'POST':
        origin = User.objects.get(id=request.POST['loged'])
        destination = User.objects.get(id=request.POST['user'])
        poke = Poke.objects.create(origin_user=origin, destination_user=destination)
        return redirect('/pokes/')