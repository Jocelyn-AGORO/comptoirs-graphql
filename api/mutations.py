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
    createStudent: StudentType = gql.django.create_mutation(StudentInput)
    updateStudent: StudentType = gql.django.update_mutation(StudentInputPartial)
    deleteStudent: StudentType = gql.django.delete_mutation(gql.NodeInput)
    createCourse: CourseType = gql.django.create_mutation(CourseInput)
    updateCourse: CourseType = gql.django.update_mutation(CourseInputPartial)
    deleteCourse: CourseType = gql.django.delete_mutation(gql.NodeInput)
    createEmployee: EmployeeType = gql.django.create_mutation(EmployeeInput)
    updateEmployee: EmployeeType = gql.django.update_mutation(EmployeeInputPartial)
    deleteEmployee: EmployeeType = gql.django.delete_mutation(gql.NodeInput)
