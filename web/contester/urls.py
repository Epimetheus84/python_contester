from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', views.login_page, name='login'),
    path('login_post', views.login_post, name='login_post'),
    path('logout', views.logout, name='logout'),
    path('exercise/show/<int:exercise_id>', views.show_exercise, name='exercise'),
    path('exercise/submit/<int:exercise_id>', views.submit_exercise, name='exercise')
]