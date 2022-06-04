from functools import partial
from django.shortcuts import render
from pyparsing import And
from rest_framework.response import Response
from rest_framework import mixins , generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Task , User
from .serializers import TaskSerializer,UserSerializer


@api_view(['GET' , "POST"])
def handle_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        tasks = TaskSerializer(tasks , many = True)
        return Response(tasks.data)
    elif request.method == "POST":
        try:
            user = User.objects.get(id = request.data['creator'])
            data_dict = request.data
            data_dict["creator"] = user
            task = Task()
            task.title = data_dict["title"]
            task.description = data_dict["description"]
            task.creator = user
            task.save()
            serializer = TaskSerializer(task, many = False)
            return Response(serializer.data, status= 201)
        except Exception as e:
            return Response({"message": str(e)} , status = 400)

@api_view(['GET' , "DELETE" , "PATCH"])
def handle_task(request,task_id):
    task = Task.objects.get(id=task_id)
    if request.method == "GET":
        try:
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist as e:
            return Response({"message" :  "task not found" },status=404)
    elif request.method == "DELETE":
        try:
            task.delete()
            return Response({"message" : "Task deleted"} , status = 204)
        except Task.DoesNotExist as e:
            return Response({"message" :  "task not found" },status=404)
    elif request.method == "PATCH":
        print(request.data)
        serializer = TaskSerializer(task , data = request.data , partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.data, status=400)


class Assign_Task(APIView):
    def get_task(self , task_id):
        try:
            task =  Task.objects.get(id=task_id) 
            return task
        except Task.DoesNotExist as e:
            raise e
    def post(self,request,task_id):
        task = self.get_task(task_id)
        user = User.objects.get(id = request.data['user'])
        serializer = UserSerializer(task.assign)
        task.assign = user
        task.save()
        return Response(serializer.data , status = 200)
    def get(self,request,task_id):
        try : 
            task = self.get_task(task_id)
            print(task)
            if task.assign is not None :
                serializer = UserSerializer(task.assign)
                return Response(serializer.data)
            return Response({"message" : "Task not assigned"} , status = 200)
        except Exception as e :
            return Response({"message" : str(e)} , status = 404)
    def delete(self , requesst,task_id):
        try:
            task = self.get_task(task_id)
            task.assign = task.creator
            task.save()
            return Response({"message" : "Task unassigned"} , status = 200)
        except Exception as e :
            return Response({"message" : str(e)} , status = 404)
