from django.db.models import Q
from graphene_django import DjangoObjectType
import graphene

from .models import Transaction
from account.models import Account
from account.schema import AccountType


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction


class Query(graphene.ObjectType):
    transactions = graphene.List(TransactionType)
    pekhom_transactions = graphene.List(TransactionType, search=graphene.String(), first=graphene.Int(), skip=graphene.Int())

    def resolve_transactions(self, info, **kwargs):
        return Transaction.objects.all()

    def resolve_pekhom_transactions(self, info, search=None, first=None, skip=None, **kwargs):
        trans = Transaction.objects.all()

        if search:
            filter = Q(pay_for__icontains=search) | Q(bank_ac_number__icontains=search)
            trans = trans.filter(filter)

        if first:
            trans = trans[:first]

        if skip:
            trans = trans[skip:]

        return trans


class CreateTransaction(graphene.Mutation):
    transactions = graphene.Field(TransactionType)
    accounts = graphene.Field(AccountType)

    class Arguments:
        id = graphene.ID()
        amount = graphene.Float()
        bank_ac_number = graphene.String()

    def mutate(self, info, id, amount, bank_ac_number):
        if not info.context.user:
            raise Exception('Login first !')

        account = Account.objects.filter(id=id).first()
        if not account:
            raise Exception('Account is not found !')

        transaction = Transaction.objects.create(amount=amount, bank_ac_number=bank_ac_number, account=account)
        return CreateTransaction(transactions=transaction, accounts=account)


class UpdateTransaction(graphene.Mutation):
    transaction = graphene.Field(TransactionType)

    class Arguments:
        id = graphene.ID()
        bank_ac_number = graphene.String()
        amount = graphene.Float()

    def mutate(self, info, id, bank_ac_number, amount):
        trans = Transaction.objects.get(id=id, bank_ac_number=bank_ac_number)
        trans.amount = amount
        trans.save()

        return UpdateTransaction(transaction=trans)


class DeleteTransaction(graphene.Mutation):
    transaction = graphene.List(TransactionType)

    class Arguments:
        id = graphene.ID()

    def mutate(self, info, id):
        trans = Transaction.objects.filter(id=id).delete()
        return DeleteTransaction(transaction=trans)


class Mutation(graphene.ObjectType):
    create_transaction = CreateTransaction.Field()
    update_transaction = UpdateTransaction.Field()
    delete_transaction = DeleteTransaction.Field()