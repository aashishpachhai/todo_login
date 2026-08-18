from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Todo
# Create your views here.
def login_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)
        if not User.objects.filter(username=username).exists():
            messages.warning(request,'Username or Password is invalid')
            print('Username or Password is invalid')
            return redirect('/login')

        user=authenticate(request,username=username,password=password)

        if user is None:
            print('incoorect')
            messages.warning(request,'Username or Password is invalid')
            return redirect('/login')

        login(request,user)
        print('Success')
        return redirect('/')
    context={'title':'Login'}
    return render(request,'login.html',context)


@login_required(login_url='/login')
def home(request):
    if request.method=='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        Todo.objects.create(title=title,description=description,user=request.user)
        return redirect('/')

    userTodo=Todo.objects.filter(user=request.user)
    context={'title':'Home','todos':userTodo}
    return render(request,'todo.html',context)

def register(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        firstname=request.POST.get('first_name')
        lastname=request.POST.get('last_name')
        password=request.POST.get('password')

        user=User.objects.filter(username=username).exists()
        if  user:
            messages.info(request,'Username already exists')
            return redirect('/register')

        newUser=User()
        newUser.first_name=firstname
        newUser.last_name=lastname
        newUser.username=username
        newUser.set_password(password)
        newUser.save()
        messages.info(request,'User created successfully')
        return redirect('/register')

    return render(request,'register.html')


def logout_user(request):
    logout(request)
    return redirect('/login')

def delete_todo(request,id):
    Todo.objects.get(id=id).delete()
    return redirect('/')

def edit_todo(request,id):
    todo=Todo.objects.get(id=id)
    context={'title':'Edit Todo','todo':todo}

    if request.method=="POST":
        title=request.POST.get("title")
        description=request.POST.get("description")
        todo.title=title
        todo.description=description
        todo.save()
        return redirect('/')

    return render(request,'edit_todo.html',context)