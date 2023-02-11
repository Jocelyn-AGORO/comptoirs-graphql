from strawberry_django_plus import gql
from typing import List, Optional
from app_2.models import *
from comptoirs_app.models import *
from .types import *

@gql.type
class Query:
    categories: List[CategorieType] = gql.django.field()
    # select a single Categorie object 
    @gql.django.field
    def categorie(self, id: int) -> CategorieType:
        return Categorie.objects.get(pk=id)


    clients: List[ClientType] = gql.django.field()
    # select a single Client object 
    @gql.django.field
    def client(self, id: int) -> ClientType:
        return Client.objects.get(pk=id)


    commandes: List[CommandeType] = gql.django.field()
    # select a single Commande object 
    @gql.django.field
    def commande(self, id: int) -> CommandeType:
        return Commande.objects.get(pk=id)


    lignes: List[LigneType] = gql.django.field()
    # select a single Ligne object 
    @gql.django.field
    def ligne(self, id: int) -> LigneType:
        return Ligne.objects.get(pk=id)


    produits: List[ProduitType] = gql.django.field()
    # select a single Produit object 
    @gql.django.field
    def produit(self, id: int) -> ProduitType:
        return Produit.objects.get(pk=id)


    students: List[StudentType] = gql.django.field()
    # select a single Student object 
    @gql.django.field
    def student(self, id: int) -> StudentType:
        return Student.objects.get(pk=id)


    courses: List[CourseType] = gql.django.field()
    # select a single Course object 
    @gql.django.field
    def course(self, id: int) -> CourseType:
        return Course.objects.get(pk=id)


    employees: List[EmployeeType] = gql.django.field()
    # select a single Employee object 
    @gql.django.field
    def employee(self, id: Optional[int]) -> EmployeeType:
        return Employee.objects.get(pk=id)


