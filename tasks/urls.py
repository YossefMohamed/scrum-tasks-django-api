from django.urls import path
from django.conf import settings
from .views import handle_tasks  , handle_task , Assign_Task

urlpatterns = [
    path("api/task/", handle_tasks),
    path("api/task/<int:task_id>", handle_task),
    path("api/task/<int:task_id>/assign", Assign_Task.as_view()),
]