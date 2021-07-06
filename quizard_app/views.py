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
        "all_quizzes": Quiz.objects.filter(category = request.POST['category_choices'])
    }

    return render(request, "dashboard.html", context)



# PROFILE PAGE
def user_page(request,username):
    
    if 'user_id' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['user_id'])
    this_user = User.objects.get(username = username)

    context = {
        'user': user,
        'this_user': this_user,
        'created_quizzes' : Quiz.objects.filter(created_by = this_user),
        'liked_quizzes': Quiz.objects.filter(liked_by = this_user),
        'quizzes_taken': Quiz.objects.filter(taken_by = this_user),
    }
    
    return render(request,'profile.html',context)

# DELETE ONCE PROJECT IS MERGED! PLACEHOLDER TO VIEW ALL QUIZZES UNTIL USER PAGE IS RUNNING
def user_quizzes(request,username):
    user = User.objects.get(id=request.session['user_id'])

    context = {
        "user": user,
        "user_quizzes": user.created_quizzes.all()
    }

    return render(request, "quizzes_list.html", context)
# ^^^^^^^^^^^^^^^

def update_user(request,username):
    if request.method == 'POST':
        this_user = User.objects.get(username = username)
        this_user.profile_photo = request.FILES.get('user_img') or this_user.profile_photo
        this_user.save()
        return redirect(f'/quizard/user/{username}')
    return redirect('/')

def delete_account(request,username):
    if 'user_id' not in request.session:
        return redirect("/")
    user_to_delete = User.objects.get(username = username)
    user_to_delete.delete()
    return redirect('/')


# QUIZZES
def quiz_form(request):
    context = {
        "category_choices": Quiz.category_choices,
        "user": User.objects.get(id=request.session['user_id']),
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
                    image=request.FILES.get(f"image{i}"),
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
        "quiz_category": quiz_category_word,
        "category_choices": Quiz.category_choices,
        # "popularity": len(quiz.liked_by.all)/len(quiz.disliked_by.all)
    }

    return render(request, "view_quiz.html", context)

def like_quiz(request,quiz_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        quiz = Quiz.objects.get(id=quiz_id)

        if user in quiz.liked_by.all():
            quiz.liked_by.remove(user)
        
        elif user in quiz.disliked_by.all():
            quiz.disliked_by.remove(user)
            quiz.liked_by.add(user)

        else:
            quiz.liked_by.add(user)

    return redirect(f'/quizard/quizzes/{quiz_id}')

def dislike_quiz(request,quiz_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        quiz = Quiz.objects.get(id=quiz_id)

        if user in quiz.disliked_by.all():
            quiz.disliked_by.remove(user)
        
        elif user in quiz.liked_by.all():
            quiz.liked_by.remove(user)
            quiz.disliked_by.add(user)

        else:
            quiz.disliked_by.add(user)

    return redirect(f'/quizard/quizzes/{quiz_id}')

def edit_quiz(request,quiz_id):
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
        "quiz_category": quiz_category_word,
        "category_choices": Quiz.category_choices,
        "range": range(25)
    }

    return render(request, "edit_quiz.html", context)

def update_quiz(request,quiz_id):
    if request.method == "POST":
        errors = Quiz.objects.validator(request.POST)
        print(errors)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)

            return redirect(f'/quizard/quizzes/{quiz_id}/edit')

        user = User.objects.get(id=request.session['user_id'])
        quiz = Quiz.objects.get(id=quiz_id)

        # QUIZ UPDATE
        quiz.name = request.POST['quiz_name']
        quiz.description = request.POST['description']
        quiz.category = request.POST['category']

        # QUESTIONS UPDATE
        for i,question in enumerate(quiz.questions.all()):
            
            question.entry = request.POST[f'entry{i+1}']
            question.answer = request.POST[f'answer{i+1}']
            question.image = request.FILES.get(f"image{i+1}") or question.image

            question.save()

        quiz.save()
    
    return redirect(f"/quizard/quizzes/{quiz_id}")

def delete_quiz(request,quiz_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.delete()

        return redirect(f"/quizard/user/{user.username}/quizzes")
    
    return redirect(f"/quizard/quizzes/{quiz_id}")

def take_quiz(request,quiz_id):
    quiz = Quiz.objects.get(id = quiz_id)
    user = User.objects.get(id=request.session['user_id'])
    quiz.taken_by.add(user)

    context = {
        'quiz': quiz,
        'user': user,
    }

    return render(request, 'take_quiz.html',context)

def mark_quiz(request,quiz_id):

    if request.method == 'POST':

        quiz = Quiz.objects.get(id = quiz_id)
        print(f"quiz: {quiz.name}")
        count = 0
        
        for i,question in enumerate(quiz.questions.all()):
            if question.answer == request.POST[f'question{i+1}']:
                count += 1
            print(f"Question: {question.entry}")
            print(f"Answer: {question.answer}")
            print(f'Entered answer: {request.POST[f"question{i+1}"]}') 

        context = {
        'quiz':quiz,
        'score': count,

        }

        return render(request, 'take_quiz.html',context)
    return redirect(f'/quizard/quizzes/{quiz_id}/take_quiz')

    #     print(i.answer)
    #     if i.answer == request.POST['question']:
    #         count = count + 1
    #     return count
    # context = {
    #     'quiz':quiz,
    #     'score': count,
    # }
    # return render(request, 'take_quiz.html',context)

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