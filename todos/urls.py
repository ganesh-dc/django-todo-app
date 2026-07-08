from django.urls import path
from . import views

urlpatterns = [
    path("", views.todo_list, name="todo_list"),
    path("signup/", views.signup, name="signup"),
    path("toggle/<int:pk>/", views.toggle_todo, name="toggle_todo"),
    path("delete/<int:pk>/", views.delete_todo, name="delete_todo"),
]
