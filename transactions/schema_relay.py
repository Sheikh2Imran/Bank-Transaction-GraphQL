import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


from .models import Transaction
from account.models import Account


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ['pay_for', 'bank_ac_number', 'amount']


class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction
        interfaces = (graphene.relay.Node,)


class RelayQuery(graphene.ObjectType):
    relay_transaction = graphene.relay.Node.Field(TransactionNode)
    relay_transactions = DjangoFilterConnectionField(TransactionNode, filterset_class=TransactionFilter)


class RelayCreateTrasaction(graphene.relay.ClientIDMutation):
    transactions = graphene.Field(TransactionNode)

    class Input:
        id = graphene.ID()
        pay_for = graphene.String()
        amount = graphene.Float()
        bank_ac_number = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        account = Account.objects.get(id=input.get('id'))
        if not account:
            raise Exception('Account Not Found')

        transaction = Transaction(pay_for=input.get('pay_for'),
                                  amount=input.get('amount'),
                                  bank_ac_number=input.get('bank_ac_number'),
                                  account=account)
        transaction.save()

        return RelayCreateTrasaction(transactions=transaction)


class RelayUpdateTransaction(graphene.relay.ClientIDMutation):
    transaction = graphene.Field(TransactionNode)

    class Input:
        id = graphene.ID()
        pay_for = graphene.String()
        amount = graphene.Float()
        bank_ac_number = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        trans = Transaction.objects.get(id=input.get('id'), bank_ac_number=input.get('bank_ac_number'))
        if not trans:
            raise Exception('Transaction not found !')

        trans.pay_for = input.get('pay_for')
        trans.amount = input.get('amount')
        trans.save()

        return RelayUpdateTransaction(transaction=trans)


class RelayDeleteTransaction(graphene.relay.ClientIDMutation):
    transaction = graphene.Field(TransactionNode)

    class Input:
        id = graphene.ID()
        bank_ac_number = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        trans = Transaction.objects.get(id=input.get('id'), bank_ac_number=input.get('bank_ac_number')).delete()
        if not trans:
            raise Exception('Transaction can not be deleted !')

        return RelayDeleteTransaction(transaciton=trans)


class RelayMutation(graphene.AbstractType):
    relay_create_transaction = RelayCreateTrasaction.Field()
    relay_update_transaction = RelayUpdateTransaction.Field()
    relay_delete_transaction = RelayDeleteTransaction.Field()