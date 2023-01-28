from strawberry_django_plus import gql
from comptoirs_app.models import *

@gql.django.input(Categorie, partial=True)
class CategorieInput:
    code: gql.auto
    libelle: gql.auto
    description: gql.auto

@gql.django.partial(Categorie)
class CategorieInputPartial(gql.NodeInput):
    code: gql.auto
    libelle: gql.auto
    description: gql.auto

@gql.django.input(Client, partial=True)
class ClientInput:
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

@gql.django.partial(Client)
class ClientInputPartial(gql.NodeInput):
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

@gql.django.input(Commande, partial=True)
class CommandeInput:
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

@gql.django.partial(Commande)
class CommandeInputPartial(gql.NodeInput):
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

@gql.django.input(Ligne, partial=True)
class LigneInput:
    id: gql.auto
    commande: gql.auto
    produit: gql.auto
    quantite: gql.auto

@gql.django.partial(Ligne)
class LigneInputPartial(gql.NodeInput):
    id: gql.auto
    commande: gql.auto
    produit: gql.auto
    quantite: gql.auto

@gql.django.input(Produit, partial=True)
class ProduitInput:
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

@gql.django.partial(Produit)
class ProduitInputPartial(gql.NodeInput):
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

