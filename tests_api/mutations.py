from strawberry_django_plus import gql
from .types import *
from .inputs import *


@gql.type
class Mutation:
    createCategorie: CategorieType = gql.django.create_mutation(CategorieInput)
    updateCategorie: CategorieType = gql.django.update_mutation(CategorieInputPartial)
    deleteCategorie: CategorieType = gql.django.delete_mutation(gql.NodeInput)
    createClient: ClientType = gql.django.create_mutation(ClientInput)
    updateClient: ClientType = gql.django.update_mutation(ClientInputPartial)
    deleteClient: ClientType = gql.django.delete_mutation(gql.NodeInput)
    createCommande: CommandeType = gql.django.create_mutation(CommandeInput)
    updateCommande: CommandeType = gql.django.update_mutation(CommandeInputPartial)
    deleteCommande: CommandeType = gql.django.delete_mutation(gql.NodeInput)
    createLigne: LigneType = gql.django.create_mutation(LigneInput)
    updateLigne: LigneType = gql.django.update_mutation(LigneInputPartial)
    deleteLigne: LigneType = gql.django.delete_mutation(gql.NodeInput)
    createProduit: ProduitType = gql.django.create_mutation(ProduitInput)
    updateProduit: ProduitType = gql.django.update_mutation(ProduitInputPartial)
    deleteProduit: ProduitType = gql.django.delete_mutation(gql.NodeInput)
