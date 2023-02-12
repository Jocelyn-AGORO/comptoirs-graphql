from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate, PageNumberPagination
from .pagination import *
from .errors import *

from .schemas import *
from .inputs import *

categorie_router = Router()


# get allcategories with pagination
@categorie_router.get('/', response=List[CategorieSchema])
@paginate(CategoriePagination)
def categories_paginated(request):
    return Categorie.objects.all()


# get the categorie with key equal to code if exists
@categorie_router.get('/{int:code}', response={200: CategorieSchema, 404: ErrorSchema})
def new_categorie(request, code: int):
    try:
        _categorie = Categorie.objects.get(pk=code)
        return 200, _categorie
    except Categorie.DoesNotExist as e:
        return 404, ErrorSchema()


# add a new categorie
@categorie_router.post('/', response={201: CategorieSchema})
def new_categorie(request, categorie: CategorieInput):
    _categorie = Categorie.objects.create(**categorie.dict())
    return _categorie


# modify the categorie with key equal to code if exists
@categorie_router.put('/{int:code}', response={200: CategorieSchema, 404: ErrorSchema})
def update_categorie(request, code: int, categorie: CategorieInput):
    try:
        _categorie = Categorie.objects.get(pk=code)
        _categorie.update(**categorie.dict())
        return 200, _categorie
    except Categorie.DoesNotExist as e:
        return 404, ErrorSchema()


# delete the categorie with key equal to code if exists
@categorie_router.delete('/{int:code}', response={404: ErrorSchema})
def delete_categorie(request, code: int):
    try:
        _categorie = Categorie.objects.get(pk=code)
        _categorie.delete()
        return {"message": True}
    except Categorie.DoesNotExist as e:
        return 404, ErrorSchema()


# Categorie cruds


@categorie_router.get('/{int:code}/produits', response={200: List[ProduitSchema], 404: ErrorSchema},
                      tags=['categories/{code}/Produits'])
def categorie_produits(request, code: int):
    try:
        _categorie = Categorie.objects.get(pk=code)
        return 200, Produit.objects.prefetch_related('categorie').filter(categorie__pk=code)
    except Categorie.DoesNotExist as e:
        return 404, ErrorSchema()


client_router = Router()


# get allclients with pagination
@client_router.get('/', response=List[ClientSchema])
@paginate(ClientPagination)
def clients_paginated(request):
    return Client.objects.all()


# get the client with key equal to code if exists
@client_router.get('/{str:code}', response={200: ClientSchema, 404: ErrorSchema})
def new_client(request, code: str):
    try:
        _client = Client.objects.get(pk=code)
        return 200, _client
    except Client.DoesNotExist as e:
        return 404, ErrorSchema()


# add a new client
@client_router.post('/', response={201: ClientSchema})
def new_client(request, client: ClientInput):
    _client = Client.objects.create(**client.dict())
    return _client


# modify the client with key equal to code if exists
@client_router.put('/{str:code}', response={200: ClientSchema, 404: ErrorSchema})
def update_client(request, code: str, client: ClientInput):
    try:
        _client = Client.objects.get(pk=code)
        _client.update(**client.dict())
        return 200, _client
    except Client.DoesNotExist as e:
        return 404, ErrorSchema()


# delete the client with key equal to code if exists
@client_router.delete('/{str:code}', response={404: ErrorSchema})
def delete_client(request, code: str):
    try:
        _client = Client.objects.get(pk=code)
        _client.delete()
        return {"message": True}
    except Client.DoesNotExist as e:
        return 404, ErrorSchema()


# Client cruds


@client_router.get('/{str:code}/commandes', response={200: List[CommandeSchema], 404: ErrorSchema},
                   tags=['clients/{code}/Commandes'])
def client_commandes(request, code: str):
    try:
        _client = Client.objects.get(pk=code)
        return 200, Commande.objects.prefetch_related('client').filter(client__pk=code)
    except Client.DoesNotExist as e:
        return 404, ErrorSchema()


commande_router = Router()


# get allcommandes with pagination
@commande_router.get('/', response=List[CommandeSchema])
@paginate(CommandePagination)
def commandes_paginated(request):
    return Commande.objects.all()


# get the commande with key equal to numero if exists
@commande_router.get('/{int:numero}', response={200: CommandeSchema, 404: ErrorSchema})
def new_commande(request, numero: int):
    try:
        _commande = Commande.objects.get(pk=numero)
        return 200, _commande
    except Commande.DoesNotExist as e:
        return 404, ErrorSchema()


# add a new commande
@commande_router.post('/', response={201: CommandeSchema})
def new_commande(request, commande: CommandeInput):
    _commande = Commande.objects.create(**commande.dict())
    return _commande


# modify the commande with key equal to numero if exists
@commande_router.put('/{int:numero}', response={200: CommandeSchema, 404: ErrorSchema})
def update_commande(request, numero: int, commande: CommandeInput):
    try:
        _commande = Commande.objects.get(pk=numero)
        _commande.update(**commande.dict())
        return 200, _commande
    except Commande.DoesNotExist as e:
        return 404, ErrorSchema()


# delete the commande with key equal to numero if exists
@commande_router.delete('/{int:numero}', response={404: ErrorSchema})
def delete_commande(request, numero: int):
    try:
        _commande = Commande.objects.get(pk=numero)
        _commande.delete()
        return {"message": True}
    except Commande.DoesNotExist as e:
        return 404, ErrorSchema()


# Commande cruds


@commande_router.get('/{int:numero}/lignes', response={200: List[LigneSchema], 404: ErrorSchema},
                     tags=['commandes/{numero}/Lignes'])
def commande_lignes(request, numero: int):
    try:
        _commande = Commande.objects.get(pk=numero)
        return 200, Ligne.objects.prefetch_related('commande').filter(commande__pk=numero)
    except Commande.DoesNotExist as e:
        return 404, ErrorSchema()


# Commande cruds


@commande_router.get('/{int:numero}/client', response={200: ClientSchema, 404: ErrorSchema},
                     tags=['commandes/{numero}/client'])
def numero_client(request, numero: int):
    try:
        _commande = Commande.objects.get(pk=numero)
        return 200, _commande.client
    except Commande.DoesNotExist as e:
        return 404, ErrorSchema()


ligne_router = Router()


# get alllignes with pagination
@ligne_router.get('/', response=List[LigneSchema])
@paginate(LignePagination)
def lignes_paginated(request):
    return Ligne.objects.all()


# get the ligne with key equal to id if exists
@ligne_router.get('/{int:id}', response={200: LigneSchema, 404: ErrorSchema})
def new_ligne(request, id: int):
    try:
        _ligne = Ligne.objects.get(pk=id)
        return 200, _ligne
    except Ligne.DoesNotExist as e:
        return 404, ErrorSchema()


# add a new ligne
@ligne_router.post('/', response={201: LigneSchema})
def new_ligne(request, ligne: LigneInput):
    _ligne = Ligne.objects.create(**ligne.dict())
    return _ligne


# modify the ligne with key equal to id if exists
@ligne_router.put('/{int:id}', response={200: LigneSchema, 404: ErrorSchema})
def update_ligne(request, id: int, ligne: LigneInput):
    try:
        _ligne = Ligne.objects.get(pk=id)
        _ligne.update(**ligne.dict())
        return 200, _ligne
    except Ligne.DoesNotExist as e:
        return 404, ErrorSchema()


# delete the ligne with key equal to id if exists
@ligne_router.delete('/{int:id}', response={404: ErrorSchema})
def delete_ligne(request, id: int):
    try:
        _ligne = Ligne.objects.get(pk=id)
        _ligne.delete()
        return {"message": True}
    except Ligne.DoesNotExist as e:
        return 404, ErrorSchema()


# Ligne cruds


@ligne_router.get('/{int:id}/commande', response={200: CommandeSchema, 404: ErrorSchema}, tags=['lignes/{id}/commande'])
def id_commande(request, id: int):
    try:
        _ligne = Ligne.objects.get(pk=id)
        return 200, _ligne.commande
    except Ligne.DoesNotExist as e:
        return 404, ErrorSchema()


# Ligne cruds


@ligne_router.get('/{int:id}/produit', response={200: ProduitSchema, 404: ErrorSchema}, tags=['lignes/{id}/produit'])
def id_produit(request, id: int):
    try:
        _ligne = Ligne.objects.get(pk=id)
        return 200, _ligne.produit
    except Ligne.DoesNotExist as e:
        return 404, ErrorSchema()


produit_router = Router()


# get allproduits with pagination
@produit_router.get('/', response=List[ProduitSchema])
@paginate(ProduitPagination)
def produits_paginated(request):
    return Produit.objects.all()


# get the produit with key equal to reference if exists
@produit_router.get('/{int:reference}', response={200: ProduitSchema, 404: ErrorSchema})
def new_produit(request, reference: int):
    try:
        _produit = Produit.objects.get(pk=reference)
        return 200, _produit
    except Produit.DoesNotExist as e:
        return 404, ErrorSchema()


# add a new produit
@produit_router.post('/', response={201: ProduitSchema})
def new_produit(request, produit: ProduitInput):
    _produit = Produit.objects.create(**produit.dict())
    return _produit


# modify the produit with key equal to reference if exists
@produit_router.put('/{int:reference}', response={200: ProduitSchema, 404: ErrorSchema})
def update_produit(request, reference: int, produit: ProduitInput):
    try:
        _produit = Produit.objects.get(pk=reference)
        _produit.update(**produit.dict())
        return 200, _produit
    except Produit.DoesNotExist as e:
        return 404, ErrorSchema()


# delete the produit with key equal to reference if exists
@produit_router.delete('/{int:reference}', response={404: ErrorSchema})
def delete_produit(request, reference: int):
    try:
        _produit = Produit.objects.get(pk=reference)
        _produit.delete()
        return {"message": True}
    except Produit.DoesNotExist as e:
        return 404, ErrorSchema()


# Produit cruds


@produit_router.get('/{int:reference}/lignes', response={200: List[LigneSchema], 404: ErrorSchema},
                    tags=['produits/{reference}/Lignes'])
def produit_lignes(request, reference: int):
    try:
        _produit = Produit.objects.get(pk=reference)
        return 200, Ligne.objects.prefetch_related('produit').filter(produit__pk=reference)
    except Produit.DoesNotExist as e:
        return 404, ErrorSchema()


# Produit cruds


@produit_router.get('/{int:reference}/categorie', response={200: CategorieSchema, 404: ErrorSchema},
                    tags=['produits/{reference}/categorie'])
def reference_categorie(request, reference: int):
    try:
        _produit = Produit.objects.get(pk=reference)
        return 200, _produit.categorie
    except Produit.DoesNotExist as e:
        return 404, ErrorSchema()


student_router = Router()


# get allstudents with pagination
@student_router.get('/', response=List[StudentSchema])
@paginate(StudentPagination)
def students_paginated(request):
    return Student.objects.all()


# get the student with key equal to id if exists
@student_router.get('/{int:id}', response={200: StudentSchema, 404: ErrorSchema})
def new_student(request, id: int):
    try:
        _student = Student.objects.get(pk=id)
        return 200, _student
    except Student.DoesNotExist as e:
        return 404, ErrorSchema()


# add a new student
@student_router.post('/', response={201: StudentSchema})
def new_student(request, student: StudentInput):
    _student = Student.objects.create(**student.dict())
    return _student


# modify the student with key equal to id if exists
@student_router.put('/{int:id}', response={200: StudentSchema, 404: ErrorSchema})
def update_student(request, id: int, student: StudentInput):
    try:
        _student = Student.objects.get(pk=id)
        _student.update(**student.dict())
        return 200, _student
    except Student.DoesNotExist as e:
        return 404, ErrorSchema()


# delete the student with key equal to id if exists
@student_router.delete('/{int:id}', response={404: ErrorSchema})
def delete_student(request, id: int):
    try:
        _student = Student.objects.get(pk=id)
        _student.delete()
        return {"message": True}
    except Student.DoesNotExist as e:
        return 404, ErrorSchema()


# Student cruds


@student_router.get('/{int:id}/courses', response={200: List[CourseSchema], 404: ErrorSchema},
                    tags=['students/{id}/Courses'])
def student_courses(request, id: int):
    try:
        _student = Student.objects.get(pk=id)
        return 200, Course.objects.prefetch_related('student').filter(student__pk=id)
    except Student.DoesNotExist as e:
        return 404, ErrorSchema()


course_router = Router()


# get allcourses with pagination
@course_router.get('/', response=List[CourseSchema])
@paginate(CoursePagination)
def courses_paginated(request):
    return Course.objects.all()


# get the course with key equal to id if exists
@course_router.get('/{int:id}', response={200: CourseSchema, 404: ErrorSchema})
def new_course(request, id: int):
    try:
        _course = Course.objects.get(pk=id)
        return 200, _course
    except Course.DoesNotExist as e:
        return 404, ErrorSchema()


# add a new course
@course_router.post('/', response={201: CourseSchema})
def new_course(request, course: CourseInput):
    _course = Course.objects.create(**course.dict())
    return _course


# modify the course with key equal to id if exists
@course_router.put('/{int:id}', response={200: CourseSchema, 404: ErrorSchema})
def update_course(request, id: int, course: CourseInput):
    try:
        _course = Course.objects.get(pk=id)
        _course.update(**course.dict())
        return 200, _course
    except Course.DoesNotExist as e:
        return 404, ErrorSchema()


# delete the course with key equal to id if exists
@course_router.delete('/{int:id}', response={404: ErrorSchema})
def delete_course(request, id: int):
    try:
        _course = Course.objects.get(pk=id)
        _course.delete()
        return {"message": True}
    except Course.DoesNotExist as e:
        return 404, ErrorSchema()


# Course cruds


@course_router.get('/{int:id}/students', response={200: List[StudentSchema], 404: ErrorSchema},
                   tags=['courses/{id}/Students'])
def course_students(request, id: int):
    try:
        _course = Course.objects.get(pk=id)
        return 200, Student.objects.prefetch_related('course').filter(course__pk=id)
    except Course.DoesNotExist as e:
        return 404, ErrorSchema()


employee_router = Router()


# get allemployees with pagination
@employee_router.get('/', response=List[EmployeeSchema])
@paginate(EmployeePagination)
def employees_paginated(request):
    return Employee.objects.all()


# get the employee with key equal to id if exists
@employee_router.get('/{int:id}', response={200: EmployeeSchema, 404: ErrorSchema})
def new_employee(request, id: int):
    try:
        _employee = Employee.objects.get(pk=id)
        return 200, _employee
    except Employee.DoesNotExist as e:
        return 404, ErrorSchema()


# add a new employee
@employee_router.post('/', response={201: EmployeeSchema})
def new_employee(request, employee: EmployeeInput):
    _employee = Employee.objects.create(**employee.dict())
    return _employee


# modify the employee with key equal to id if exists
@employee_router.put('/{int:id}', response={200: EmployeeSchema, 404: ErrorSchema})
def update_employee(request, id: int, employee: EmployeeInput):
    try:
        _employee = Employee.objects.get(pk=id)
        _employee.update(**employee.dict())
        return 200, _employee
    except Employee.DoesNotExist as e:
        return 404, ErrorSchema()


# delete the employee with key equal to id if exists
@employee_router.delete('/{int:id}', response={404: ErrorSchema})
def delete_employee(request, id: int):
    try:
        _employee = Employee.objects.get(pk=id)
        _employee.delete()
        return {"message": True}
    except Employee.DoesNotExist as e:
        return 404, ErrorSchema()


# Employee cruds


@employee_router.get('/{int:id}/employees', response={200: List[EmployeeSchema], 404: ErrorSchema},
                     tags=['employees/{id}/Employees'])
def employee_employees(request, id: int):
    try:
        _employee = Employee.objects.get(pk=id)
        return 200, Employee.objects.prefetch_related('employee').filter(employee__pk=id)
    except Employee.DoesNotExist as e:
        return 404, ErrorSchema()


# Employee cruds


@employee_router.get('/{int:id}/employee', response={200: EmployeeSchema, 404: ErrorSchema},
                     tags=['employees/{id}/employee'])
def id_employee(request, id: int):
    try:
        _employee = Employee.objects.get(pk=id)
        return 200, _employee.employee
    except Employee.DoesNotExist as e:
        return 404, ErrorSchema()


# Employee cruds


@employee_router.get('/{int:id}/employee', response={200: EmployeeSchema, 404: ErrorSchema},
                     tags=['employees/{id}/employee'])
def id_employee(request, id: int):
    try:
        _employee = Employee.objects.get(pk=id)
        return 200, _employee.employee
    except Employee.DoesNotExist as e:
        return 404, ErrorSchema()
