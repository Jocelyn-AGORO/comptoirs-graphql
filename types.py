from strawberry_django_plus import gql
from typing import List, Optional
from comptoirs_app.models import *

@gql.django.type(Categorie)
class CategorieType:
    code: gql.auto
    libelle: gql.auto
    description: gql.auto

    produits: 'List[ProduitType]'

@gql.django.type(Client)
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

@gql.django.type(Commande)
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
    def produits(self, root, info):
        return Commande.objects.produit_set.all()
    lignes: 'List[LigneType]'

@gql.django.type(Ligne)
class LigneType:
    id: gql.auto
    commande: gql.auto
    produit: gql.auto
    quantite: gql.auto

    commande: 'CommandeType'
    produit: 'ProduitType'

@gql.django.type(Produit)
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
    def commandes(self, root, info):
        return Produit.objects.commande_set.all()
    lignes: 'List[LigneType]'

