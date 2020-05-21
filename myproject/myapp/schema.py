import graphene
from graphene_django import DjangoObjectType

from myapp.models import UserModel, Article, Reporter, Publication

class UserType(DjangoObjectType):
    class Meta:
        model = UserModel

class ReporterType(DjangoObjectType):
    class Meta:
        model = Reporter

class PublicationType(DjangoObjectType):
    class Meta:
        model = Publication

class ArticleType(DjangoObjectType):
    class Meta:
        model = Article

class Query(graphene.ObjectType):
    user = graphene.Field(UserType,id=graphene.Int(),name=graphene.String(),last_name=graphene.String())
    users = graphene.List(UserType)

    reporter = graphene.Field(ReporterType,id=graphene.Int(),first_name=graphene.String(),last_name=graphene.String())
    reporters = graphene.List(ReporterType)

    publication = graphene.Field(PublicationType,id=graphene.Int(),title=graphene.String())
    publications = graphene.List(PublicationType)
    
    article = graphene.Field(ArticleType,id=graphene.Int(),headline=graphene.String())
    articles = graphene.List(ArticleType)

    def resolve_users(self, info):
        return UserModel.objects.all()

    def resolve_reporters(self, info):
        return Reporter.objects.all()

    def resolve_publications(self, info):
        return Publication.objects.all()

    def resolve_articles(self, info):
        return ArticleType.objects.all()

    def resolve_publication(self,info,**kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            return Publication.objects.get(pk=id)
        
        if title is not None:
            return Publication.objects.get(title=title)

        return None

    def resolve_reporter(self, info, **kwargs):
        id = kwargs.get('id')
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')

        if id is not None:
            return Reporter.objects.get(pk=id)

        if first_name is not None:
            return Reporter.objects.get(first_name=first_name)

        if last_name is not None:
            return Reporter.objects.get(last_name=last_name)

        return None

class CreateUser(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    last_name = graphene.String()

    class Arguments:
        name = graphene.String()
        last_name = graphene.String()

    def mutate(self, info, name, last_name):
        user = UserModel(name=name, last_name=last_name)
        user.save()

        return CreateUser(
            id=user.id,
            name=user.name,
            last_name=user.last_name,
        )

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
    )
