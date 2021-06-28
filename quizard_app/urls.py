from django.urls import path
from . import views

urlpatterns = [
    # LOGIN FUNCTIONS
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    # HOME PAGE FUNCTIONS
    path('quizard', views.dashboard),


    # PROFILE PAGE FUNCTIONS
    path('quizard/user/<str:username>', views.user_page),
    path('quizard/user/<str:username>/update', views.update_user),
    path('quizard/user/<str:username>/destroy', views.delete_account),


    # QUIZZES FUNCTIONS
    path('quizard/quizzes/new', views.create_quiz),
    path('quizard/quizzes/<int:quiz_id>', views.view_quiz),
    path('quizard/quizzes/<int:quiz_id>/like', views.like_quiz),
    path('quizard/quizzes/<int:quiz_id>/dislike', views.dislike_quiz),
    path('quizard/quizzes/<int:quiz_id>/update', views.update_quiz),
    path('quizard/quizzes/<int:quiz_id>/destroy', views.delete_quiz),

    # FLASHCARDS
    path('quizard/quizzes/<int:quiz_id>/flashcard/new', views.create_flashcard),
    path('quizard/quizzes/<int:quiz_id>/flashcard/<int:flashcard_id>/update', views.update_flashcard),
    path('quizard/quizzes/<int:quiz_id>/flashcard/<int:flashcard_id>/destroy', views.delete_flashcard)
]





# urlpatterns = [
#     path('', views.index),
#     path('register', views.create_user),
#     path('login',views.log_in),
#     path('logoff',views.log_out),

#     path('dashboard',views.dashboard),
#     path(‘quizzes/new’, views.create_quiz),
#     path(‘quizzes/<int:id>’, views.this_quiz),
#     path(‘quizzes/<int:id>/like’, views.like_quiz),
#     path(‘quizzes/<int:id>/dislike’, views.dislike_quiz),
#     path(‘quizzes/<int:id>/update’, views.update_quiz),
#     path(‘quizzes/<int:id>/destroy’, views.delete_quiz),
#     path(‘quizzes/<int:id>/flashcard/new’, views.create_flashcard),
#     path(‘quizzes/<int:id>/flashcard/update’, views.update_flashcard),
#     path(‘quizzes/<int:id>/flashcard/destroy’, views.delete_flashcard),
#     path(‘pages/<int:id>’, views.user_page),
#     path(‘pages/<int:id>/picture’, views.update_user_picture),
#     path(‘pages/<int:id>/destroy’, views.delete_account),
# ]