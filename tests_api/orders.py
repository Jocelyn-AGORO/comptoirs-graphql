from strawberry_django_plus import gql
from comptoirs_app.models import *

@gql.django.ordering.order(Categorie)
class CategorieOrder:
    code: gql.auto
    libelle: gql.auto
    description: gql.auto
    produit: 'ProduitOrder'

@gql.django.ordering.order(Client)
class ClientOrder:
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
    commande: 'CommandeOrder'

@gql.django.ordering.order(Commande)
class CommandeOrder:
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
    client: 'ClientOrder'
    produit: 'ProduitOrder'
    ligne: 'LigneOrder'

@gql.django.ordering.order(Ligne)
class LigneOrder:
    id: gql.auto
    commande: gql.auto
    produit: gql.auto
    quantite: gql.auto
    commande: 'CommandeOrder'
    produit: 'ProduitOrder'

@gql.django.ordering.order(Produit)
class ProduitOrder:
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
    categorie: 'CategorieOrder'
    commande: 'CommandeOrder'
    ligne: 'LigneOrder'

