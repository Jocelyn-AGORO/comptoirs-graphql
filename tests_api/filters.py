from strawberry_django_plus import gql
from comptoirs_app.models import *

@gql.django.filters.filter(Categorie, lookups=True)
class CategorieFilter:
    code: gql.auto
    libelle: gql.auto
    description: gql.auto
    produit: 'ProduitFilter'

@gql.django.filters.filter(Client, lookups=True)
class ClientFilter:
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
    commande: 'CommandeFilter'

@gql.django.filters.filter(Commande, lookups=True)
class CommandeFilter:
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
    client: 'ClientFilter'
    produit: 'ProduitFilter'
    ligne: 'LigneFilter'

@gql.django.filters.filter(Ligne, lookups=True)
class LigneFilter:
    id: gql.auto
    commande: gql.auto
    produit: gql.auto
    quantite: gql.auto
    commande: 'CommandeFilter'
    produit: 'ProduitFilter'

@gql.django.filters.filter(Produit, lookups=True)
class ProduitFilter:
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
    categorie: 'CategorieFilter'
    commande: 'CommandeFilter'
    ligne: 'LigneFilter'

