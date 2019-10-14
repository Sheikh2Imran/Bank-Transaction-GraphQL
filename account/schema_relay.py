import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Account


class AccountFilter(django_filters.FilterSet):
    class Meta:
        model = Account
        fields = ['identifier', 'connect_id']


class AccountNode(DjangoObjectType):
    class Meta:
        model = Account
        interfaces = (graphene.relay.Node, )


class RelayQuery(graphene.ObjectType):
    relay_account = graphene.relay.Node.Field(AccountNode)
    relay_accounts = DjangoFilterConnectionField(AccountNode, filterset_class=AccountFilter)


class RelayCreateAccount(graphene.relay.ClientIDMutation):
    # create a new account
    accounts = graphene.Field(AccountNode)

    class Input:
        username = graphene.String()
        identifier = graphene.String()
        circuit_id = graphene.String()
        connect_id = graphene.String()
        mobile_number = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user
        if not user:
            raise Exception('You are not logged in !')
        if user.is_anonymous:
            raise Exception('User is anonymous !')

        account = Account(
            username=input.get('username'),
            identifier=input.get('identifier'),
            circuit_id=input.get('circuit_id'),
            connect_id=input.get('connect_id'),
            mobile_number=input.get('mobile_number'),
            created_by=user,
        )
        account.save()

        return RelayCreateAccount(accounts=account)


class RelayUpdateAccount(graphene.relay.ClientIDMutation):
    # update account
    account = graphene.Field(AccountNode)

    class Input:
        id = graphene.ID()
        username = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        account = Account.objects.get(id=input.get('id'))
        if not account:
            raise Exception('Account can not be found')

        account.username = input.get('username')
        account.save()

        return RelayUpdateAccount(account=account)


class RelayDeleteAccount(graphene.relay.ClientIDMutation):
    # delete an account
    account = graphene.Field(AccountNode)

    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(self, info, **input):
        account = Account.objects.filter(id=input.get('id')).delete()

        return RelayDeleteAccount(account=account)


class RelayMutation(graphene.AbstractType):
    relay_create_account = RelayCreateAccount.Field()
    relay_update_account = RelayUpdateAccount.Field()
    relay_delete_account = RelayDeleteAccount.Field()

