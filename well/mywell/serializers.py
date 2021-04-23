from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import *
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class projectSerializer(serializers.ModelSerializer):
    class Meta:
        model = project
        fields = '__all__'


class CustomGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGroup
        fields = '__all__'



class project_detailSerializer(serializers.ModelSerializer):
    class Meta:
        model = project_detail
        fields = '__all__'