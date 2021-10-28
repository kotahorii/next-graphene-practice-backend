from django.db import models
import graphene
from graphene_django.types import DjangoObjectType
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
        fields = ("id", "user", "followings", "created_on")


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    profiles = graphene.List(ProfileType)
    profile = graphene.Field(ProfileType, id=graphene.Int())

    def resolve_profile(root, info, **kwargs):
        id = kwargs.get('id')
        return Profile.objects.get(pk=id)

    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_profiles(root, info, **kwargs):
        return Profile.objects.all()


class CreateUserMutation(graphene.Mutation):

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(root, info, **kwargs):
        user = User(
            username=kwargs.get('username'),
            email=kwargs.get('email'),
        )
        user.set_password(kwargs.get('password'))
        user.save()
        return CreateUserMutation(user=user)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    create_user = CreateUserMutation.Field()
