from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

# LOGIN/REGISTER

def index(request):
    return render(request, "login_reg.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')

        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id

        return redirect('/noted')

    return redirect('/')

def login(request):
    if request.method=="POST":
        
        if not User.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, "Invalid Email/Password")
            return redirect('/')

        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id

        return redirect('/noted')

    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')


# HOME PAGE

def dashboard(request):
    pass


# PROFILE PAGE
def user_page(request,username):
    pass

def update_user(request,username):
    pass

def delete_account(request,username):
    pass


# QUIZZES
def create_quiz(request):
    pass

def view_quiz(request,quiz_id):
    pass

def like_quiz(request,quiz_id):
    pass

def dislike_quiz(request,quiz_id):
    pass

def update_quiz(request,quiz_id):
    pass

def delete_quiz(request,quiz_id):
    pass

# FLASHCARDS
def create_flashcard(request,quiz_id):
    pass

def update_flashcard(request,quiz_id,flashcard_id):
    pass

def delete_flashcard(request,quiz_id,flashcard_id):
    pass