from decimal import Decimal
from datetime import datetime, date, time
from ninja import Schema
from typing import Optional

class CategorieInput(Schema):
    libelle: Optional[str]
    description: Optional[str]


class ClientInput(Schema):
    societe: Optional[str]
    contact: Optional[str]
    fonction: Optional[str]
    adresse: Optional[str]
    ville: Optional[str]
    region: Optional[str]
    code_postal: Optional[str]
    pays: Optional[str]
    telephone: Optional[str]
    fax: Optional[str]


class CommandeInput(Schema):
    saisiele: Optional[date]
    envoyeele: Optional[date]
    port: Optional[Decimal]
    destinataire: Optional[str]
    adresse_livraison: Optional[str]
    ville_livraison: Optional[str]
    region_livraison: Optional[str]
    code_postal_livraison: Optional[str]
    pays_livraison: Optional[str]
    remise: Optional[Decimal]


class LigneInput(Schema):
    quantite: Optional[int]


class ProduitInput(Schema):
    nom: Optional[str]
    fournisseur: Optional[int]
    quantite_par_unite: Optional[str]
    prix_unitaire: Optional[Decimal]
    unites_en_stock: Optional[int]
    unites_commandees: Optional[int]
    niveau_de_reappro: Optional[int]
    indisponible: Optional[int]


class StudentInput(Schema):
    name: Optional[str]
    age: Optional[int]


class CourseInput(Schema):
    title: Optional[str]
    volume: Optional[int]


class EmployeeInput(Schema):
    title: Optional[str]




