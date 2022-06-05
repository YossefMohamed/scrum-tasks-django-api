from django.urls import path
from django.conf import settings
from .views import handle_tasks  , handle_task , Assign_Task , Register , Login , GetUserData

urlpatterns = [
    path("api/task/", handle_tasks),
    path("api/task/<int:task_id>", handle_task),
    path("api/task/<int:task_id>/assign", Assign_Task.as_view()),
    path("api/register", Register.as_view()),
    path("api/login", Login.as_view()),
    path("api/user", GetUserData.as_view())
]