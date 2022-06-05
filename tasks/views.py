from functools import partial
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import mixins , generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Task , User
from .serializers import TaskSerializer,UserSerializer
import jwt 
import datetime

def check_token(token):
    try:
        
        data = jwt.decode(token , "secret" , algorithms=['HS256'])
        return data["user_id"]
    except:
        raise AuthenticationFailed("Invalid Token")


@api_view(['GET' , "POST"])
def handle_tasks(request):
    print(request.headers)
    if request.method == 'GET':
        try :
            token = request.headers["Authorization"]
            token = token.split(" ")[1]
            user_id = check_token(token)
            tasks = Task.objects.filter(creator= user_id)
            tasks = TaskSerializer(tasks , many = True)
            return Response(tasks.data)
        except Exception as e:
            return Response({"message" : str(e)})
    elif request.method == "POST":
        try:
            token = request.headers["Authorization"]
            token = token.split(" ")[1]
            user_id = check_token(token)
            print(user_id)
            user = User.objects.get(id = user_id)
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
    try:
        task = Task.objects.get(id=task_id)
        token = request.headers["Authorization"]
        token = token.split(" ")[1]
        user_id = check_token(token)
        if task.creator != user_id:
            return Response({"message" : "You are not allowed to edit this task"} , status = 403)
        if request.method == "GET":
            return Response(serializer.data)
        elif request.method == "DELETE":
                task.delete()
                return Response({"message" : "Task deleted"} , status = 204)
        elif request.method == "PATCH":
            serializer = TaskSerializer(task , data = request.data , partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.data, status=400)
    except Exception as e:
        return Response({"message" : str(e)})


class Assign_Task(APIView):
    def get_task(self , task_id, request) :
        try:
            task = Task.objects.get(id=task_id)
            token = request.headers["Authorization"]
            token = token.split(" ")[1]
            user_id = check_token(token)
            task =  Task.objects.get(id=task_id) 
            if task.creator.id != user_id:
                raise Exception("You are not allowed to edit this task")
            return task
        except Task.DoesNotExist as e:
            raise e
    def post(self,request,task_id):
        task = self.get_task(task_id, request)
        user = User.objects.get(id = request.data['user'])
        serializer = UserSerializer(task.assign)
        task.assign = user
        task.save()
        return Response(serializer.data , status = 200)
    def get(self,request,task_id):
        try : 
            task = self.get_task(task_id , request)
            print(task)
            if task.assign is not None :
                serializer = UserSerializer(task.assign)
                return Response(serializer.data)
            return Response({"message" : "Task not assigned"} , status = 200)
        except Exception as e :
            return Response({"message" : str(e)} , status = 404)
    def delete(self , request,task_id):
        try:
            task = self.get_task(task_id , request)
            task.assign = task.creator
            task.save()
            return Response({"message" : "Task unassigned"} , status = 200)
        except Exception as e :
            return Response({"message" : str(e)} , status = 404)



class Register(APIView):
    def post(sef , request):
        try:
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status = 201)
            return Response(serializer.errors , status = 400)
        except Exception as e:
            return Response({"message" : str(e)} , status = 400)


class Login(APIView):
    def post(self , request):
        try:
            user = User.objects.get(username = request.data['username'])
            if not user.check_password(request.data['password']):
                return Response({"message" : "username or Password are wrong"} , status = 400)
            payload = {
                'user_id' : user.id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 60)
            }
            token = jwt.encode(payload , "secret" , algorithm = "HS256")
            serializer = UserSerializer(user)
            return Response({"user" : serializer.data , "token" : token } , status = 200)
        except Exception as e:
            print(str(e))
            return Response({"message" : str(e)} , status = 400)



class GetUserData(APIView):
    def get(self , request):
        try:
            token = request.headers["Authorization"]
            token = token.split(" ")[1]
            user_id = check_token(token)
            user = User.objects.get(id = user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data , status = 200)
        except Exception as e:
            return Response({"message" : str(e)} , status = 400)
    def patch(self,request):
        try:
            token = request.headers["Authorization"]
            token = token.split(" ")[1]
            user_id = check_token(token)
            user = User.objects.get(id = user_id)
            serializer = UserSerializer(user , data = request.data , partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status = 200)
            return Response(serializer.errors , status = 400)
        except Exception as e:
            return Response({"message" : str(e)} , status = 400)