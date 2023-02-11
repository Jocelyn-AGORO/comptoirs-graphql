from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from django.db import models as dj_models
from django.db.models import Count, Sum, Avg, Min, Max, StdDev, Variance
import os


def map_rel(related_obj):
    value = repr(related_obj).split()
    return value[0][1:-1], value[1][0:-1].split('.')[1].capitalize()


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


def get_key(model):
    return model._meta.pk.name


def get_field_type(field):
    if field.is_relation:
        return ''
    elif isinstance(field, dj_models.AutoField):
        return 'int'
    elif isinstance(field, dj_models.BigAutoField):
        return 'int'
    elif isinstance(field, dj_models.BooleanField):
        return 'bool'
    elif isinstance(field, dj_models.CharField):
        return 'str'
    elif isinstance(field, dj_models.TextField):
        return 'str'
    elif isinstance(field, dj_models.DateField):
        return 'date'
    elif isinstance(field, dj_models.DateTimeField):
        return 'datetime'
    elif isinstance(field, dj_models.DecimalField):
        return 'Decimal'
    elif isinstance(field, dj_models.DurationField):
        return 'timedelta'
    elif isinstance(field, dj_models.EmailField):
        return 'str'
    elif isinstance(field, dj_models.FloatField):
        return 'float'
    elif isinstance(field, dj_models.IntegerField):
        return 'int'
    elif isinstance(field, dj_models.BigIntegerField):
        return 'int'
    elif isinstance(field, dj_models.NullBooleanField):
        return 'bool'
    elif isinstance(field, dj_models.PositiveIntegerField):
        return 'int'
    elif isinstance(field, dj_models.PositiveSmallIntegerField):
        return 'int'
    elif isinstance(field, dj_models.SmallIntegerField):
        return 'int'
    elif isinstance(field, dj_models.TimeField):
        return 'time'
    else:
        return 'None'


def get_all_relationships(models):
    relationships = {}
    for model_class in models:
        relationships.update(get_relationships_3_1(model_class))
    return relationships


def get_relationships_3_1(model_class):
    relationships = {}
    for field in model_class._meta.get_fields():
        if field.is_relation and not field.auto_created:
            related_model = field.related_model
            if field.many_to_many:
                relationship = 'ManyToMany'
                through_model = field.remote_field.through
                relationships.setdefault(model_class.__name__, []).append(
                    (relationship, related_model.__name__, through_model.__name__))
                relationships.setdefault(related_model.__name__, []).append(
                    ('ManyToMany', model_class.__name__, through_model.__name__))
            elif field.one_to_one:
                relationship = 'OneToOne'
                relationships.setdefault(model_class.__name__, []).append((relationship, related_model.__name__))
                relationships.setdefault(related_model.__name__, []).append(('OneToOne', model_class.__name__))
            else:
                relationship = 'ManyToOne' if field.one_to_many else 'Self' if related_model == model_class else 'OneToMany'
                relationships.setdefault(model_class.__name__, []).append((relationship, related_model.__name__))
                reverse_relationship = 'ManyToOne' if relationship == 'OneToMany' else 'OneToMany'
                relationships.setdefault(related_model.__name__, []).append(
                    (reverse_relationship, model_class.__name__))

    return relationships


def reverse_rels(rels: dict):
    equivalent = {
        'OneToMany': 'ManyToOne',
        'ManyToOne': 'OneToMany',
        'ManyToMany': 'ManyToMany',
        'OneToOne': 'OneToOne',
        'Self': 'Self'
    }
    reverse_rels = {model: [] for model in rels.keys()}
    # print(reverse_rels)
    for model in rels.keys():
        # print(rels.get(model))
        for relation in rels.get(model):
            if len(relation) >= 3:
                reverse_rels[relation[1]].append((equivalent[relation[0]], model, *relation[2:]))
            else:
                reverse_rels[relation[1]].append((equivalent[relation[0]], model))
    # print(reverse_rels)
    return reverse_rels


def all_rels(rels: dict, r_rels: dict):
    all = {}
    for model in rels.keys():
        all[model] = list(set(rels[model] + r_rels[model]))
    return all


def resolve_all_rels(models):
    rels = get_all_relationships(models)
    r_rels = reverse_rels(rels)
    a_rels = all_rels(rels, r_rels)
    return a_rels


def resolve_relations(relations, model):
    equivalent = {
        'OneToMany': lambda model_: f"    {model_.lower()}: Optional['{model_}Schema']\n",
        'ManyToOne': lambda model_: f"    {model_.lower()}s: Optional[List['{model_}Schema']]\n",
        'ManyToMany': lambda model_: f"    {model_.lower()}s: Optional[List['{model_}Schema']]\n",
        'OneToOne': lambda model_: f"    {model_.lower()}: Optional['{model_}Schema']\n",
        'Self': lambda model_: f"    parent{model_.capitalize()}: Optional['{model_}Schema']\n"
    }
    code = ""
    for relation in relations.get(model.__name__):
        code += equivalent[relation[0]](relation[1])
    return code


def generate_schemas(obj, models, relations, filename=f"{str(settings.BASE_DIR)}/schemas.py"):
    code = ""
    code += "from decimal import Decimal\n"
    code += "from datetime import datetime, date, time\n"
    for app in get_generated_apps():
        code += f"from {app}.models import *\n"
    # generer les input body
    code += f"from .inputs import *\n"
    code += "from ninja import ModelSchema\n"
    # end of import
    code += "from typing import List, Optional\n"
    code += "\n"
    generate_file(filename, code)
    # reset code to empty string
    code = ""
    for model in models:
        # resolve related models
        code += f"class {model.__name__}Schema(ModelSchema):\n"
        # code += resolve_relations(relations, model) + '\n'
        # define the class for the graphql type
        code += f"    class Config:\n"
        code += f"        model = {model.__name__}\n"
        code += f'        model_fields = "__all__"\n\n'
        # code += f"        depth = 1\n\n"
    code += f"\n\n"
    if filename == "stdout":
        obj.stdout.write(obj.style.NOTICE(code))
    else:
        generate_file(filename, code)


def generate_inputs(obj, models, filename=f"{str(settings.BASE_DIR)}/inputs.py"):
    code = ""
    code += "from decimal import Decimal\n"
    code += "from datetime import datetime, date, time\n"
    code += "from ninja import Schema\n"
    # end of import
    code += "from typing import Optional\n"
    code += "\n"
    generate_file(filename, code)
    # reset code to empty string
    code = ""
    for model in models:
        # resolve related models
        code += f"class {model.__name__}Input(Schema):\n"
        for field in model._meta.fields:
            if field != model._meta.pk:
                code += f"    {field.name}: Optional[{get_field_type(field)}]\n"
        code += "\n\n"
        # # define the class for the graphql type
        # code += f"    class Config:\n"
        # code += f"        model = {model.__name__}\n\n"
        # code += f'        model_fields = "__all__"\n\n'
        # code += f'        model_exclude = ["{model._meta.pk.name}"]\n\n'
    code += f"\n\n"
    if filename == "stdout":
        obj.stdout.write(obj.style.NOTICE(code))
    else:
        generate_file(filename, code)

# get all data for a model
def generate_crud_all(obj, model, filename):
    code = ""
    # end of import
    code += f"# {model.__name__} cruds\n"
    code += f"@{model.__name__.lower()}_router.get('/', response=List[{model.__name__}Schema])\n"
    code += f"def all_{model.__name__.lower()}s(request):\n"
    code += f"    return {model.__name__}.objects.all()\n"
    code += "\n\n"
    if filename == "stdout":
        obj.stdout.write(obj.style.NOTICE(code))
    else:
        generate_file(filename, code)


def generate_crud_paginate(obj, model, filename):
    code = ""
    # end of import
    code += f"# {model.__name__} cruds\n"
    code += f"@{model.__name__.lower()}_router.get('/', response=List[{model.__name__}Schema])\n"
    code += "@paginate(PageNumberPagination)\n"
    code += f"def {model.__name__.lower()}s_paginated(request):\n"
    code += f"    return {model.__name__}.objects.all()\n"
    code += "\n\n"
    if filename == "stdout":
        obj.stdout.write(obj.style.NOTICE(code))
    else:
        generate_file(filename, code)


def generate_crud_one(obj, model, filename):
    code = ""
    # end of import
    code += f"# {model.__name__} cruds\n"
    code += f"@{model.__name__.lower()}_router.get('/{{{get_field_type(model._meta.pk)}:{get_key(model)}}}', response={model.__name__}Schema)\n"
    code += f"def {model.__name__.lower()}(request, {get_key(model)}: {get_field_type(model._meta.pk)}):\n"
    code += f"    return {model.__name__}.objects.get(pk={get_key(model)})\n"
    code += "\n\n"
    if filename == "stdout":
        obj.stdout.write(obj.style.NOTICE(code))
    else:
        generate_file(filename, code)


def generate_crud_add(obj, model, filename):
    code = ""
    # end of import
    code += f"# {model.__name__} cruds\n"
    code += f"@{model.__name__.lower()}_router.post('/', response={model.__name__}Schema)\n"
    code += f"def new{model.__name__.lower()}(request, {model.__name__.lower()}: {model.__name__}Input ):\n"
    code += f"    _{model.__name__.lower()} = {model.__name__}.objects.create(**{model.__name__.lower()}.dict())\n"
    code += f"    return _{model.__name__.lower()}\n"
    code += "\n\n"
    if filename == "stdout":
        obj.stdout.write(obj.style.NOTICE(code))
    else:
        generate_file(filename, code)


def generate_crud_update(obj, model, filename):
    code = ""
    # end of import
    code += f"# {model.__name__} cruds\n"
    code += f"@{model.__name__.lower()}_router.put('/{{{get_field_type(model._meta.pk)}:{get_key(model)}}}')\n"
    code += f"def update{model.__name__.lower()}(request, {get_key(model)}: {get_field_type(model._meta.pk)}, {model.__name__.lower()}: {model.__name__}Input ):\n"
    code += f"    _{model.__name__.lower()} = get_object_or_404({model.__name__}, id={get_key(model)})\n"
    code += f"    for attr, new_value in {model.__name__.lower()}.dict().items():\n"
    code += f"        setattr(_{model.__name__.lower()}, attr, new_value)\n"
    code += f"    _{model.__name__.lower()}.save()\n"
    code += f'    return {{"success": True}}\n'
    code += "\n\n"
    if filename == "stdout":
        obj.stdout.write(obj.style.NOTICE(code))
    else:
        generate_file(filename, code)


def generate_crud_delete(obj, model, filename):
    code = ""
    # end of import
    code += f"# {model.__name__} cruds\n"

    code += f"@{model.__name__.lower()}_router.delete('/{{{get_field_type(model._meta.pk)}:{get_key(model)}}}')\n"
    code += f"def delete_{model.__name__.lower()}(request, {get_key(model)}: {get_field_type(model._meta.pk)}):\n"
    code += f"    _{model.__name__.lower()} = get_object_or_404({model.__name__}, id={get_key(model)})\n"
    code += f"    {model.__name__}.objects.delete()\n"
    code += '    return {"success": True}\n'
    code += "\n\n"
    if filename == "stdout":
        obj.stdout.write(obj.style.NOTICE(code))
    else:
        generate_file(filename, code)


def one(model, model_):
    code = ""
    code += f"{model_.lower()}', response={model_}Schema, tags=['{model.__name__.lower()}s/{{{get_key(model)}}}/{model_.lower()}'])\n"
    code += f"def {model.__name__.lower()}_{model_.lower()}(request, {get_key(model)}:{get_field_type(model._meta.pk)}):\n"
    code += f"    _{model.__name__.lower()} = {model.__name__}.objects.get(pk=id)\n"
    code += f"    return _{model.__name__.lower()}.{model_.lower()}\n"
    code += "\n"
    return code


def many(model, model_):
    code = ""
    code += f"{model_.lower()}s', response=List[{model_}Schema], tags=['{model.__name__.lower()}s/{{{get_key(model)}}}/{model_.lower()}s'])\n"
    code += f"def {model.__name__.lower()}_{model_.lower()}s(request, {get_key(model)}:{get_field_type(model._meta.pk)}):\n"
    code += f"    return {model_}.objects.prefetch_related('{model.__name__.lower()}').filter({model.__name__.lower()}__pk={get_key(model)})\n"
    code += "\n"
    return code


def resolve_rels_paths(relations, model):
    equivalent = {
        'OneToMany': one,
        'ManyToOne': many,
        'ManyToMany': many,
        'OneToOne': one,
        'Self': one
    }
    code = ""
    for relation in relations.get(model.__name__):
        code += f"# {model.__name__} cruds\n"
        code += f"@{model.__name__.lower()}_router.get('/{{int:id}}/"
        code += equivalent[relation[0]](model, relation[1])
    return code


def generate_crud_related(obj, relations, model, filename):
    code = resolve_rels_paths(relations, model)
    code += "\n"
    if filename == "stdout":
        obj.stdout.write(obj.style.NOTICE(code))
    else:
        generate_file(filename, code)


def generate_crud(obj, relations, model, filename):
    code = ""
    generate_crud_all(obj, model, filename)
    generate_crud_paginate(obj, model, filename)
    generate_crud_one(obj, model, filename)
    generate_crud_add(obj, model, filename)
    generate_crud_update(obj, model, filename)
    generate_crud_delete(obj, model, filename)
    generate_crud_related(obj, relations, model, filename)
    return code


def generate_cruds(obj, relations, models, filename):
    code = ""
    code += "from django.shortcuts import get_object_or_404\n"
    code += "from ninja import Router\n"
    code += "from ninja.pagination import paginate, PageNumberPagination\n"
    code += "from .schemas import *\n"
    code += "from .inputs import *\n\n"
    generate_file(filename, code)
    for model in models:
        generate_file(filename, f"{model.__name__.lower()}_router = Router()\n")
        generate_crud(obj, relations, model, filename)


def generate_crud_api(obj, models, relations, api_name: str = 'ninja_api'):
    base_dir = f"{str(settings.BASE_DIR)}/{api_name}"
    try:
        os.mkdir(base_dir)
    except Exception as e:
        print(f"Error when creating the file ... {e}")
    # set the directory as a module
    generate_file(base_dir + "/__init__.py", "")
    # generate inputs
    # generate filters
    generate_inputs(obj, models, filename=base_dir + "/inputs.py")
    # generate orders
    generate_schemas(obj, models, relations, filename=base_dir + "/schemas.py")
    # web services
    generate_cruds(obj, relations, models, filename=base_dir + "/api.py")
    from platform import system
    from os import system as sys
    if system().lower() == "windows":
        main_app = '\\' + str(settings.BASE_DIR).split('\\')[-1] + '\\'
    else:
        main_app = '/' + str(settings.BASE_DIR).split('/')[-1] + '/'
    code = "\n\n\n"
    code += "from ninja import NinjaAPI\n"
    for model in models:
        code += f"from {api_name}.api import {model.__name__.lower()}_router\n"
    code += "\napi =  NinjaAPI()\n\n"
    # add router for each model
    for model in models:
        code += f"api.add_router('/{model.__name__.lower()}s/', {model.__name__.lower()}_router, tags=['{model.__name__.lower()}s'])\n"
    code += "urlpatterns.append(path('api/', api.urls))\n"
    generate_file(str(settings.BASE_DIR) + main_app + 'urls.py', code)
    # res = sys('python manage.py runserver')
    # print(res)


# generate relations from models
models = [model for model in apps.get_models() if repr(model).startswith("<class 'django.") is False]
relations = resolve_all_rels(models)


class Command(BaseCommand):
    help = "Django Ninja Command line Interface for Code Generation"

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
        # add target module for the generated crud api
        parser.add_argument('-t', '--target', nargs=1, type=str,
                            help="Specify the path to generate the crud api")

    def handle(self, *args, **kwargs):
        global models
        global relations
        commands = kwargs['generate']
        # returns all models of installed apps
        if commands[1] == "models":
            print(models)
        # generate Strawberry types from django models
        if commands[1] == "schemas":
            # code = "from ninja import ModelSchema\n"
            # code += "from typing import List, Optional\n"
            # for app in get_generated_apps():
            #     code += f"from {app}.models import *\n"
            # # end of import
            # code += "\n"
            code = ""
            generate_file(f"{str(settings.BASE_DIR)}/schemas.py", code)
            # optional argument --args
            if kwargs['models']:
                models = [model for model in apps.get_models() if
                          model.__name__ in [name.capitalize() for name in kwargs['models']]]
                # put code in the console
                if kwargs.get('stream'):
                    generate_schemas(self, models, relations, filename="stdout")
                # default put code in python file
                else:
                    generate_schemas(self, models, relations)
            # retrieve each model
            else:
                if kwargs.get('stream'):
                    generate_schemas(self, models, relations, filename="stdout")
                else:
                    generate_schemas(self, models, relations)
            self.stdout.write(self.style.SUCCESS("types are successfully generated"))

        if commands[1] == "api":
            generate_crud_api(self, models, relations)


def map_rel(related_obj):
    value = repr(related_obj).split()
    return value[0][1:-1], value[1][0:-1].split('.')[1].capitalize()
