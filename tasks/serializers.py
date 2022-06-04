from rest_framework import serializers
from tasks.models import Task , User


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'created_at', 'updated_at', 'completed', 'pinned', 'creator' , "assign")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'age')



