import json
import datetime
import graphene

# class History(graphene.ObjectType):
#     totalcount = graphene.Int()

# class Commit(graphene.ObjectType):
#     history = graphene.Field(History, since = graphene.DateTime(datetime.datetime.today()))

class Query(graphene.ObjectType):
    test = graphene.Boolean()

    def resolve_is_staff(self, info):
        return True

schema = graphene.Schema(query=Query)

result = schema.execute(
    '''
    {
        is_staff
    }

    '''
)

print(result.data.items())
