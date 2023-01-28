from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
import os


def get_generated_apps() -> list[str]:
    path = settings.BASE_DIR
    dirs = os.listdir(path)
    dirs = [dir for dir in dirs if os.path.isdir(os.path.join(path, dir))]
    dirs = [dir for dir in dirs if os.path.isfile(os.path.join(path.joinpath(dir), 'apps.py'))]
    return dirs


def generate_file(filename: str, code: str):
    with open(filename, "a") as f:
        # write the generated code to the file
        f.write(code)


def map_rel(related_obj):
    value = repr(related_obj).split()
    return value[0][1:-1], value[1][0:-1].split('.')[1].capitalize()


def process_relations(models):
    # get django relations ManyToOneRel, OneToOneRel, ManyToManyRel
    types = [(model.__name__, [map_rel(related_obj) for related_obj in model._meta.related_objects if
                               related_obj != ()]) for model in models]
    # get models without relations
    unrelated = []
    for type in types:
        # if the relations fields list is empty
        if not type[1]:
            unrelated.append(type)
    # check if the unrelated models does not have OneToManyRel With other models
    reverse = []
    for type in types:
        #  relation[0] -> Relationship , relation[1] -> Model,stored in a tuple (Relationship, Model)
        for relation in type[1]:
            if relation[0] == 'ManyToOneRel':
                # determine the reverse relationship for instance (Parent, (OneToMany, Child)) => (Child, (ManyToOne, Parent))
                reverse.append((relation[1], ('OneToManyRel', type[0])))
            if relation[0] == 'OneToOneRel':
                # determine the reverse relationship for instance (User, (OneToOne, Account)) => (Account, (OneToOne, User))
                reverse.append((relation[1], ('OneToOneRel', type[0])))
            if relation[0] == 'ManyToManyRel':
                # determine the reverse relationship for instance (Product, (ManyToMany, Order)) => (Order, (ManyToMany, Product))
                reverse.append((relation[1], ('ManyToManyRel', type[0])))
    # for each models with it related model and the type of relation
    # this is a list of tuple, the first element is a model, the second element is tuple of (ReverseRelationShip, ReverseModel)
    reverse_keys = {type[0] for type in reverse}
    final_reverse = []
    for unrel in reverse_keys:
        # regrouped = ()
        related = []
        for type in reverse:
            if type[0] == unrel:
                related.append(type[1])
        regrouped = (unrel, related)
        final_reverse.append(regrouped)
    final_reverse += [type for type in types if type[1]]
    relations = final_reverse  # {model[0]: model[1] for model in final_reverse}
    return relations


def resolve_related_fields(relations, model):
    code = ""
    for relation in relations:
        if relation[0].lower() == model.lower():
            for related in relation[1]:
                if related[0].lower() == 'manytoonerel':
                    code += f"    {related[1].lower()}s: 'List[{related[1]}Type]'\n"
                if related[0].lower() == 'onetoonerel':
                    code += f"    {related[1].lower()}: '{related[1]}Type'\n"
                if related[0].lower() == 'onetomanyrel':
                    code += f"    {related[1].lower()}: '{related[1]}Type'\n"
                if related[0].lower() == 'manytomanyrel':
                    # automatically generate code for the reverse relationship
                    code += f"    @gql.django.field\n"
                    code += f"    def {related[1].lower()}s(self, root, info):\n"
                    code += f"        return {model}.objects.{related[1].lower()}_set.all()\n"

    return code


def resolve_related_filters(relations, model, related):
    code = ""
    if related:
        for relation in relations:
            if relation[0].lower() == model.lower():
                for related in relation[1]:
                    code += f"    {related[1].lower()}: '{related[1]}Filter'\n"
    return code


def resolve_related_orders(relations, model, related):
    code = ""
    if related:
        for relation in relations:
            if relation[0].lower() == model.lower():
                for related in relation[1]:
                    code += f"    {related[1].lower()}: '{related[1]}Order'\n"
    return code


def generate_type(obj, models, relations, filename=f"{str(settings.BASE_DIR)}/types.py"):
    for model in models:
        code = f"""@gql.django.type"""
        # add the model to the type annotation
        code += f"({model.__name__})\n"
        # define the class for the graphql type
        code += f"class {model.__name__}Type:\n"
        # add each field of the models in django
        for field in model._meta.fields:
            code += f"    {field.name}: gql.auto\n"
        # end of fields declaration
        code += "\n"
        code += resolve_related_fields(relations, model.__name__) + '\n'
        if filename == "stdout":
            obj.stdout.write(obj.style.NOTICE(code))
        else:
            generate_file(filename, code)


def generate_inputs(obj, models, filename=f"{str(settings.BASE_DIR)}/inputs.py"):
    for model in models:
        code = f"""@gql.django.input({model.__name__}, partial=True)\n"""
        # define the class for the graphql type
        code += f"class {model.__name__}Input:\n"
        # add each field of the models in django
        for field in model._meta.fields:
            code += f"    {field.name}: gql.auto\n"
        # end of fields declaration
        code += "\n"
        if filename == "stdout":
            obj.stdout.write(obj.style.NOTICE(code))
        else:
            generate_file(filename, code)


def generate_filters(obj, models, relations, related=True, filename=f"{str(settings.BASE_DIR)}/filters.py"):
    for model in models:
        code = f"""@gql.django.filters.filter({model.__name__}, lookups=True)\n"""
        # define the class for the graphql type
        code += f"class {model.__name__}Filter:\n"
        # add each field of the models in django
        for field in model._meta.fields:
            code += f"    {field.name}: gql.auto\n"
        code += resolve_related_filters(relations, model.__name__, related) + '\n'
        if filename == "stdout":
            obj.stdout.write(obj.style.NOTICE(code))
        else:
            generate_file(filename, code)


def generate_orders(obj, models, relations, related=True, filename=f"{str(settings.BASE_DIR)}/orders.py"):
    for model in models:
        code = f"""@gql.django.ordering.order({model.__name__})\n"""
        # define the class for the graphql type
        code += f"class {model.__name__}Order:\n"
        # add each field of the models in django
        for field in model._meta.fields:
            code += f"    {field.name}: gql.auto\n"
        code += resolve_related_filters(relations, model.__name__, related) + '\n'
        if filename == "stdout":
            obj.stdout.write(obj.style.NOTICE(code))
        else:
            generate_file(filename, code)


def generate_query_type(obj, models, filename=f"{str(settings.BASE_DIR)}/queries.py"):
    code = "from strawberry_django_plus import gql\n"
    code += "from .types import *\n"
    # end of imports
    code += "\n"
    for model in models:
        code += f"""@gql.type\n"""
        # define the class for the graphql query type
        code += f"class {model.__name__}Query:\n"
        # field resolver for all objects
        code += f"    @gql.field\n"
        code += f"    def all(self) -> List[{model.__name__}Type]:\n"
        code += f"        return {model.__name__}.objects.all()\n\n\n"
        # field resolver for a unique object
        code += f"    @gql.field\n"
        code += f"    def where(self, id: int) -> {model.__name__}Type:\n"
        code += f"        return {model.__name__}.objects.get(pk=id)\n\n\n"
        # field resolver for a unique object
        code += f"    @gql.field\n"
        code += f"    def count(self) -> int:\n"
        code += f"        return {model.__name__}.objects.count()\n\n\n"
        if filename == "stdout":
            obj.stdout.write(obj.style.NOTICE(code))
        else:
            generate_file(filename, code)


def generate_query(obj, models, filename=f"{str(settings.BASE_DIR)}/queries.py"):
    code = "from strawberry_django_plus import gql\n"
    code += "from .types import *\n"
    # end of imports
    code += "\n"
    code += f"""@gql.type\n"""
    # define the class for the graphql query type
    code += f"class Query:\n"
    for model in models:
        # field resolver for all types
        code += f"    {model.__name__.lower()}s: List[{model.__name__}Type] = gql.django.field()\n"
        code += f"    # select a single {model.__name__} object \n"
        code += f"    @gql.django.field\n"
        code += f"    def {model.__name__.lower()}(self, id: int) -> {model.__name__}Type:\n"
        code += f"        return {model.__name__}.objects.get(pk=id)\n\n\n"
    if filename == "stdout":
        obj.stdout.write(obj.style.NOTICE(code))
    else:
        generate_file(filename, code)


def generate_mutation(filename=f"{str(settings.BASE_DIR)}/mutations.py"):
    code = "from strawberry_django_plus import gql\n\n\n"
    code += "@gql.type"
    code += "class Mutation:"
    code += "    pass:"


def generate_crud_api():
    pass


def generate_aggregations():
    pass


def generate_relations():
    pass


def generate_joins():
    pass


# generate relations from models
models = [model for model in apps.get_models() if repr(model).startswith("<class 'django.") is False]
relations = process_relations(models)


class Command(BaseCommand):
    help = "Strawberry Command line Interface for Code Generation"

    def add_arguments(self, parser):
        # gets models for installed apps
        parser.add_argument('generate', nargs=2, type=str, help="Get models of all installed apps")
        # optionnal arguments
        parser.add_argument('-m', '--models', nargs='+', type=str, help="Specify your models list to get types with "
                                                                        "--models SomeModel AnotherModel ...")
        parser.add_argument('-s', '--stream', type=str, help="Specify that generated code is send to a file ex : "
                                                             "--stream stdout")
        # for each models
        parser.add_argument('-ex', '--exclude', nargs='+', type=str,
                            help="Specify models fields to exclude a django model ")

    def handle(self, *args, **kwargs):
        global models
        global relations
        commands = kwargs['generate']
        # returns all models of installed apps
        if commands[1] == "models":
            print(models)
        # generate Strawberry types from django models
        if commands[1] == "types":
            code = "from strawberry_django_plus import gql\n"
            code += "from typing import List, Optional\n"
            for app in get_generated_apps():
                code += f"from {app}.models import *\n"
            # end of import
            code += "\n"
            generate_file(f"{str(settings.BASE_DIR)}/types.py", code)
            # optional argument --args
            if kwargs['models']:
                models = [model for model in apps.get_models() if
                          model.__name__ in [name.capitalize() for name in kwargs['models']]]
                # put code in the console
                if kwargs.get('stream'):
                    generate_type(self, models, relations, filename="stdout")
                # default put code in python file
                else:
                    generate_type(self, models, relations)
            # retrieve each model
            else:
                if kwargs.get('stream'):
                    generate_type(self, models, relations, filename="stdout")
                else:
                    generate_type(self, models, relations)
            self.stdout.write(self.style.SUCCESS("types are successfully generated"))
        # generate Types Queries for each specified model in the list --models
        if commands[1] == "typeQuery":
            # optional argument --args
            if kwargs['models']:
                models = [model for model in apps.get_models() if
                          model.__name__ in [name.capitalize() for name in kwargs['models']]]
                if kwargs.get('stream'):
                    generate_query_type(self, models, filename="stdout")
                else:
                    generate_query_type(self, models)
            # retrieve each model
            else:
                if kwargs.get('stream'):
                    generate_query_type(self, models, filename="stdout")
                else:
                    generate_query_type(self, models)
        # generate type query resolver for specified for the specified models
        if commands[1] == "resolvers":
            generate_query(self, models)
        # generate the specified for the specified models
        if commands[1] == "field":
            pass
        # generate an input type for the specified models
        if commands[1] == "inputs":
            code = "from strawberry_django_plus import gql\n"
            code += "from typing import Optional\n"
            for app in get_generated_apps():
                code += f"from {app}.models import *\n"
            # end of import
            code += "\n"
            generate_file(f"{str(settings.BASE_DIR)}/inputs.py", code)
            # optional argument --args
            if kwargs['models']:
                models = [model for model in apps.get_models() if
                          model.__name__ in [name.capitalize() for name in kwargs['models']]]
                # put code in the console
                if kwargs.get('stream'):
                    generate_inputs(self, models, filename="stdout")
                # default put code in python file
                else:
                    generate_inputs(self, models)
            # retrieve each model
            else:
                if kwargs.get('stream'):
                    generate_inputs(self, models, filename="stdout")
                else:
                    generate_inputs(self, models)
            self.stdout.write(self.style.SUCCESS("inputs are successfully generated"))

        # generate a filter type for specified for the specified models
        if commands[1] == "filters":
            code = "from strawberry_django_plus import gql\n"
            for app in get_generated_apps():
                code += f"from {app}.models import *\n"
            # end of import
            code += "\n"
            generate_file(f"{str(settings.BASE_DIR)}/filters.py", code)
            # optional argument --args
            if kwargs['models']:
                models = [model for model in apps.get_models() if
                          model.__name__ in [name.capitalize() for name in kwargs['models']]]
                # put code in the console
                if kwargs.get('stream'):
                    generate_filters(self, models, relations, related=False, filename="stdout")
                # default put code in python file
                else:
                    generate_filters(self, models, relations, related=False)
            # retrieve each model
            else:
                if kwargs.get('stream'):
                    generate_filters(self, models, relations, filename="stdout")
                else:
                    generate_filters(self, models, relations)
            self.stdout.write(self.style.SUCCESS("filters are successfully generated"))

        # generate an input partial type for specified for the specified models
        if commands[1] == "orders":
            code = "from strawberry_django_plus import gql\n"
            for app in get_generated_apps():
                code += f"from {app}.models import *\n"
            # end of import
            code += "\n"
            generate_file(f"{str(settings.BASE_DIR)}/orders.py", code)
            # optional argument --args
            if kwargs['models']:
                models = [model for model in apps.get_models() if
                          model.__name__ in [name.capitalize() for name in kwargs['models']]]
                # put code in the console
                if kwargs.get('stream'):
                    generate_orders(self, models, relations, related=False, filename="stdout")
                # default put code in python file
                else:
                    generate_orders(self, models, relations, related=False)
            # retrieve each model
            else:
                if kwargs.get('stream'):
                    generate_orders(self, models, relations, filename="stdout")
                else:
                    generate_orders(self, models, relations)
            self.stdout.write(self.style.SUCCESS("filters are successfully generated"))

        # generate an input partial type for specified for the specified models
        if commands[1] == "partials":
            pass
