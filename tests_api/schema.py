from strawberry import Schema
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from .queries import Query
from .mutations import Mutation


graphql_schema = Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ]
)
