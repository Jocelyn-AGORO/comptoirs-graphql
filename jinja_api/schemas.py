from decimal import Decimal
from datetime import datetime, date, time
from app_2.models import *
from comptoirs_app.models import *
from .inputs import *
from ninja import ModelSchema
from typing import List, Optional

class CategorieSchema(ModelSchema):
    class Config:
        model = Categorie
        model_fields = "__all__"

class ClientSchema(ModelSchema):
    class Config:
        model = Client
        model_fields = "__all__"

class CommandeSchema(ModelSchema):
    class Config:
        model = Commande
        model_fields = "__all__"

class LigneSchema(ModelSchema):
    class Config:
        model = Ligne
        model_fields = "__all__"

class ProduitSchema(ModelSchema):
    class Config:
        model = Produit
        model_fields = "__all__"

class StudentSchema(ModelSchema):
    class Config:
        model = Student
        model_fields = "__all__"

class CourseSchema(ModelSchema):
    class Config:
        model = Course
        model_fields = "__all__"

class EmployeeSchema(ModelSchema):
    class Config:
        model = Employee
        model_fields = "__all__"



