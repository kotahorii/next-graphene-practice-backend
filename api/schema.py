from django.db import models
import graphene
from graphene_django.types import DjangoObjectType
import graphql_jwt
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from .models import Profile, User
from graphql_relay import from_global_id


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "password", "username")


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ("id", "user", "followings", "created_on")


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    profiles = graphene.List(ProfileType)
    profile = graphene.Field(ProfileType, id=graphene.Int())

    def resolve_profile(root, info, **input):
        id = input.get('id')
        return Profile.objects.get(pk=id)

    def resolve_users(root, info, **input):
        return User.objects.all()

    def resolve_profiles(root, info, **input):
        return Profile.objects.all()


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(root, info, **input):
        user = User(
            username=input.get('username'),
            email=input.get('email'),
        )
        user.set_password(input.get('password'))
        user.save()
        return CreateUserMutation(user=user)


class CreateProfileMutation(graphene.Mutation):
    profile = graphene.Field(ProfileType)

    def mutate(root, info, **input):
        profile = Profile(
            user=info.context.user.id
        )
        return CreateProfileMutation(profile=profile)


class UpdateProfileMutation(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        followings = graphene.List(graphene.UUID)

    profile = graphene.Field(ProfileType)

    def mutate(root, info, **input):
        profile = Profile.objects.get(id=input.get('id'))

        if input.get('followings') is not None:
            followings_set = []
            for followings_id in input.get('followings'):
                followings_object = User.objects.get(id=followings_id)
                followings_set.append(followings_object)
            profile.followings.set(followings_set)
        profile.save()
        
        return UpdateProfileMutation(profile=profile)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    create_user = CreateUserMutation.Field()
    create_profile = CreateProfileMutation.Field()
    update_profile = UpdateProfileMutation.Field()
