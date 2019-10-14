from graphene_django import DjangoObjectType
import graphene

from .models import Account
from users.schema import UserType


class AccountType(DjangoObjectType):
    class Meta:
        model = Account


class Query(graphene.ObjectType):
    accounts = graphene.List(AccountType)

    def resolve_accounts(self, info, **kwargs):
        return Account.objects.all()


class CreateAccount(graphene.Mutation):
    accounts = graphene.Field(AccountType)
    created_by = graphene.Field(UserType)

    class Arguments:
        username = graphene.String()
        identifier = graphene.String()
        circuit_id = graphene.String()
        connect_id = graphene.String()
        mobile_number = graphene.String()

    def mutate(self, info, username, identifier, circuit_id, connect_id, mobile_number):
        user = info.context.user or None

        account = Account(
            username=username,
            identifier=identifier,
            circuit_id=circuit_id,
            connect_id=connect_id,
            mobile_number=mobile_number,
            created_by=user,
        )
        account.save()
        return CreateAccount(accounts=account, created_by=account.created_by)


class UpdateAccount(graphene.Mutation):
    account = graphene.Field(AccountType)

    class Arguments:
        id = graphene.ID()
        username = graphene.String()

    def mutate(self, info, id, username):
        account = Account.objects.get(id=id)
        if not account:
            raise Exception('Account not found !')

        account.username = username
        account.save()

        return UpdateAccount(account=account)


class DeleteAccount(graphene.Mutation):
    account = graphene.Field(AccountType)

    class Arguments:
        id = graphene.ID()

    def mutate(self, info, id):
        account = Account.objects.get(id=id).delete()
        return DeleteAccount(account=account)


class Mutation(graphene.ObjectType):
    create_account = CreateAccount.Field()
    update_account = UpdateAccount.Field()
    delete_account = DeleteAccount.Field()