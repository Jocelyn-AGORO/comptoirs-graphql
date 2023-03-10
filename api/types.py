from strawberry_django_plus import gql
from app_2.models import *
from comptoirs_app.models import *
from typing import List, Optional

from .inputs import *
from .filters import *
from .orders import *


@gql.django.type(Categorie, filters=CategorieFilter, order=CategorieOrder)
class CategorieType:
    code: gql.auto
    libelle: gql.auto
    description: gql.auto

    produits: 'List[ProduitType]'


@gql.django.type(Client, filters=ClientFilter, order=ClientOrder)
class ClientType:
    code: gql.auto
    societe: gql.auto
    contact: gql.auto
    fonction: gql.auto
    adresse: gql.auto
    ville: gql.auto
    region: gql.auto
    code_postal: gql.auto
    pays: gql.auto
    telephone: gql.auto
    fax: gql.auto

    commandes: 'List[CommandeType]'


@gql.django.type(Commande, filters=CommandeFilter, order=CommandeOrder)
class CommandeType:
    numero: gql.auto
    client: gql.auto
    saisiele: gql.auto
    envoyeele: gql.auto
    port: gql.auto
    destinataire: gql.auto
    adresse_livraison: gql.auto
    ville_livraison: gql.auto
    region_livraison: gql.auto
    code_postal_livraison: gql.auto
    pays_livraison: gql.auto
    remise: gql.auto

    client: 'ClientType'

    @gql.django.field
    def produits(self, root, info) -> List['ProduitType']:
        return root.produits()

    lignes: 'List[LigneType]'


@gql.django.type(Ligne, filters=LigneFilter, order=LigneOrder)
class LigneType:
    id: gql.auto
    commande: gql.auto
    produit: gql.auto
    quantite: gql.auto

    commande: 'CommandeType'
    produit: 'ProduitType'


@gql.django.type(Produit, filters=ProduitFilter, order=ProduitOrder)
class ProduitType:
    reference: gql.auto
    nom: gql.auto
    fournisseur: gql.auto
    categorie: gql.auto
    quantite_par_unite: gql.auto
    prix_unitaire: gql.auto
    unites_en_stock: gql.auto
    unites_commandees: gql.auto
    niveau_de_reappro: gql.auto
    indisponible: gql.auto

    categorie: 'CategorieType'

    @gql.django.field
    def commandes(self, root, info) -> List['CommandeType']:
        return root.commandes()

    lignes: 'List[LigneType]'


@gql.django.type(Student, filters=StudentFilter, order=StudentOrder)
class StudentType:
    id: gql.auto
    name: gql.auto
    age: gql.auto

    @gql.django.field
    def courses(self, root, info) -> List['CourseType']:
        print(root)
        return root.courses


@gql.django.type(Course, filters=CourseFilter, order=CourseOrder)
class CourseType:
    id: gql.auto
    title: gql.auto
    volume: gql.auto

    @gql.django.field
    def students(self, root, info) -> List['StudentType']:
        return root.students()


@gql.django.type(Employee, filters=EmployeeFilter, order=EmployeeOrder)
class EmployeeType:
    id: gql.auto
    title: gql.auto
    supervisor: gql.auto

    parentEmployee: 'EmployeeType' = lambda self, root: root.supervisor

    @gql.django.field
    def employeeChildren(self, root) -> 'List[EmployeeType]':
        return root.employee_set.all()
