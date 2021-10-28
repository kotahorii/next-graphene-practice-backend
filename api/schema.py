from django.db import models
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
import graphql_jwt
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from .models import Profile


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "password")


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ("id", "user_prof", "followings", "created_on")


class Query(graphene.ObjectType):
    @login_required
    def
