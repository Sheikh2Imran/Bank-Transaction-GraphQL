import graphene
import graphql_jwt

import users.schema
import account.schema
import account.schema_relay
import transactions.schema
import transactions.schema_relay


class Query(users.schema.Query, account.schema.Query, transactions.schema.Query, account.schema_relay.RelayQuery,
            transactions.schema_relay.RelayQuery, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, account.schema.Mutation, transactions.schema.Mutation,
               account.schema_relay.RelayMutation, transactions.schema_relay.RelayMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)