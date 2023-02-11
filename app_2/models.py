from django.db import models


# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=255, null=True)
    age = models.PositiveIntegerField()

    courses = models.ManyToManyField('Course')


class Course(models.Model):
    title = models.CharField(max_length=255, null=True)
    volume = models.PositiveIntegerField()

    def students(self):
        return self.student_set.all()


class Employee(models.Model):
    title = models.CharField(max_length=255, null=True)
    supervisor = models.ForeignKey('self', on_delete=models.PROTECT, null=True)


# def get_relationships(model_class):
#     relationships = {}
#     for field in model_class._meta.get_fields():
#         if field.is_relation and not field.auto_created:
#             related_model = field.related_model
#             if field.many_to_many:
#                 relationship = 'ManyToMany'
#                 through_model = field.remote_field.through
#                 relationships.setdefault(model_class, []).append((relationship, related_model, through_model))
#             elif field.one_to_one:
#                 relationship = 'OneToOne'
#                 relationships.setdefault(model_class, []).append((relationship, related_model))
#             else:
#                 relationship = 'ManyToOne' if field.one_to_many else 'OneToMany'
#                 relationships.setdefault(model_class, []).append((relationship, related_model))
#             if related_model == model_class:
#                 relationship = 'Self'
#                 relationships.setdefault(model_class, []).append((relationship, related_model))
#     return relationships

def get_relationships_1(model_class):
    relationships = {}
    for field in model_class._meta.get_fields():
        if field.is_relation and not field.auto_created:
            related_model = field.related_model
            if field.many_to_many:
                relationship = 'ManyToMany'
                through_model = field.remote_field.through
                relationships.setdefault(model_class.__name__, []).append(
                    (relationship, related_model.__name__, through_model))
            elif field.one_to_one:
                relationship = 'OneToOne'
                relationships.setdefault(model_class.__name__, []).append((relationship, related_model.__name__))
            else:
                relationship = 'ManyToOne' if field.one_to_many else 'Self' if related_model == model_class else 'OneToMany'
                relationships.setdefault(model_class.__name__, []).append((relationship, related_model.__name__))
    return relationships


def get_relationships(model_class):
    relationships = {}
    for field in model_class._meta.get_fields():
        if field.is_relation and not field.auto_created:
            related_model = field.related_model
            if field.many_to_many:
                relationship = 'ManyToMany'
                through_model = field.remote_field.through
                relationships.setdefault(model_class.__name__, []).append(
                    (relationship, related_model.__name__, through_model))
            elif field.one_to_one:
                relationship = 'OneToOne'
                relationships.setdefault(model_class.__name__, []).append((relationship, related_model.__name__))
            else:
                relationship = 'ManyToOne' if field.one_to_many else 'OneToMany'
                relationships.setdefault(model_class.__name__, []).append((relationship, related_model.__name__))
            if related_model == model_class:
                relationship = 'Self'
                relationships.setdefault(model_class.__name__, []).append((relationship, related_model.__name__))
    return relationships


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
    print(reverse_rels)
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
