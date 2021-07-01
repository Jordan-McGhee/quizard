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

        return redirect('/quizard')

    return redirect('/')

def login(request):
    if request.method=="POST":
        
        if not User.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, "Invalid Email/Password")
            return redirect('/')

        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id

        return redirect('/quizard')

    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')


# HOME PAGE

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "all_quizzes": Quiz.objects.all()
    }

    return render(request, "dashboard.html", context)

def sort_category(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "all_quizzes": Quiz.objects.order_by('category')
    }

    return render(request, "dashboard.html", context)



# PROFILE PAGE
def user_page(request,username):
    pass

def update_user(request,username):
    pass

def delete_account(request,username):
    pass


# QUIZZES
def quiz_form(request):
    context = {
        "category_choices": Quiz.category_choices,
        "range": range(25)
    }
    return render(request, "create_quiz.html", context)

def create_quiz(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        errors = Quiz.objects.validator(request.POST)
        
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect(f'/quizard/quizzes/new')

        quiz = Quiz.objects.create(name=request.POST['quiz_name'], description=request.POST['description'], created_by=user, category = request.POST['category'])

        for i in range(1,26):
            if request.POST[f'entry{i}'] != "":
                Question.objects.create(
                    quiz = quiz,
                    entry=request.POST[f'entry{i}'],
                    image=request.FILES.get("image"),
                    answer=request.POST[f'answer{i}']
                    )

        print(quiz.description)

        return redirect(f'/quizard/quizzes/{quiz.id}')

    return redirect('/quizard')

def view_quiz(request,quiz_id):
    user = User.objects.get(id=request.session['user_id'])
    quiz = Quiz.objects.get(id=quiz_id)

    # IS A STR NUMBER FROM CATEGORY CHOICES IN MODELS
    quiz_category = quiz.category
    # CONVERTS TO NUM AND SUBTRACTS 1 TO GRAB RIGHT INDEX
    quiz_category_num = int(quiz_category)-1
    # GRABS WORD FROM TUPLE PAIR TO GIVE US THE CATEGORY NAME FOR THIS QUIZ
    quiz_category_word = Quiz.category_choices[quiz_category_num][1]

    context = {
        "user": user,
        "quiz": quiz,
        "quiz_category": quiz_category_word
        # "popularity": len(quiz.liked_by.all)/len(quiz.disliked_by.all)
    }

    return render(request, "view_quiz.html", context)

def like_quiz(request,quiz_id):
    pass

def dislike_quiz(request,quiz_id):
    pass

def edit_quiz(request,quiz_id):

    context = {
        "quiz": Quiz.objects.get(id=quiz_id),
        "user": User.objects.get(id=request.session['user_id']),
        "category_choices": Quiz.category_choices,
        "range": range(25)
    }

    return render(request, "edit_quiz.html", context)

def update_quiz(request,quiz_id):
    pass

def delete_quiz(request,quiz_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.delete()

        return redirect(f"/quizard/user/{user.username}")
    
    return redirect(f"/quizard/quizzes/{quiz_id}")

# FLASHCARDS
def create_flashcard(request,quiz_id):
    pass

def edit_flashcard(request,quiz_id,flashcard_id):
    pass

def update_flashcard(request,quiz_id,flashcard_id):
    pass

def delete_flashcard(request,quiz_id,flashcard_id):
    if request.method == "POST":
        flashcard = Question.objects.get(id=flashcard_id)
        flashcard.delete()

    return redirect(f"/quizard/quizzes/{quiz_id}")