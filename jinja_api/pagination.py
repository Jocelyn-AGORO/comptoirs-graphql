from ninja.pagination import PaginationBase
from ninja import Schema
from typing import List, Any
from django.conf import settings


class Input(Schema):
    page: int
    size: int


def resolve_links(pagination: Input, total: int, resource_name: str):
    base_path = settings.API_BASE_PATH + resource_name
    links = {
        "prev": f"{base_path}/?page={pagination.page - 1}&size={pagination.size}" if pagination.page > 1 else f"{base_path}/?page=1&size={pagination.size}",
        "first": f"{base_path}/?page=1&size={pagination.size}",
        "last": f"{base_path}/?page={round(total / pagination.size)}&size={pagination.size}",
        "next": f"{base_path}/?page={pagination.page + 1}&size={pagination.size}" if pagination.page <= int(
            total / pagination.size) else f"{base_path}/?page={int(total / pagination.size)}&size={pagination.size}"
    }
    return links



class CategoriePagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        page: int
        size: int

    class Output(Schema):
        categories: List[Any]  # `items` is a default attribute
        total: int
        page: int
        per_page: int
        links: dict

    items_attribute: str = "categories"

    def resolve_links(self, pagination: Input, total: int):
        return resolve_links(pagination, total, self.items_attribute)

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        size = pagination.size
        total = queryset.count()
        return {
            'categories': queryset[(page - 1) * size: page * size],
            'total': total,
            'page': page,
            'per_page': size,
            'links': {
                **self.resolve_links(pagination, total)
            }
        }


class ClientPagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        page: int
        size: int

    class Output(Schema):
        clients: List[Any]  # `items` is a default attribute
        total: int
        page: int
        per_page: int
        links: dict

    items_attribute: str = "clients"

    def resolve_links(self, pagination: Input, total: int):
        return resolve_links(pagination, total, self.items_attribute)

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        size = pagination.size
        total = queryset.count()
        return {
            'clients': queryset[(page - 1) * size: page * size],
            'total': total,
            'page': page,
            'per_page': size,
            'links': {
                **self.resolve_links(pagination, total)
            }
        }


class CommandePagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        page: int
        size: int

    class Output(Schema):
        commandes: List[Any]  # `items` is a default attribute
        total: int
        page: int
        per_page: int
        links: dict

    items_attribute: str = "commandes"

    def resolve_links(self, pagination: Input, total: int):
        return resolve_links(pagination, total, self.items_attribute)

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        size = pagination.size
        total = queryset.count()
        return {
            'commandes': queryset[(page - 1) * size: page * size],
            'total': total,
            'page': page,
            'per_page': size,
            'links': {
                **self.resolve_links(pagination, total)
            }
        }


class LignePagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        page: int
        size: int

    class Output(Schema):
        lignes: List[Any]  # `items` is a default attribute
        total: int
        page: int
        per_page: int
        links: dict

    items_attribute: str = "lignes"

    def resolve_links(self, pagination: Input, total: int):
        return resolve_links(pagination, total, self.items_attribute)

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        size = pagination.size
        total = queryset.count()
        return {
            'lignes': queryset[(page - 1) * size: page * size],
            'total': total,
            'page': page,
            'per_page': size,
            'links': {
                **self.resolve_links(pagination, total)
            }
        }


class ProduitPagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        page: int
        size: int

    class Output(Schema):
        produits: List[Any]  # `items` is a default attribute
        total: int
        page: int
        per_page: int
        links: dict

    items_attribute: str = "produits"

    def resolve_links(self, pagination: Input, total: int):
        return resolve_links(pagination, total, self.items_attribute)

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        size = pagination.size
        total = queryset.count()
        return {
            'produits': queryset[(page - 1) * size: page * size],
            'total': total,
            'page': page,
            'per_page': size,
            'links': {
                **self.resolve_links(pagination, total)
            }
        }


class StudentPagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        page: int
        size: int

    class Output(Schema):
        students: List[Any]  # `items` is a default attribute
        total: int
        page: int
        per_page: int
        links: dict

    items_attribute: str = "students"

    def resolve_links(self, pagination: Input, total: int):
        return resolve_links(pagination, total, self.items_attribute)

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        size = pagination.size
        total = queryset.count()
        return {
            'students': queryset[(page - 1) * size: page * size],
            'total': total,
            'page': page,
            'per_page': size,
            'links': {
                **self.resolve_links(pagination, total)
            }
        }


class CoursePagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        page: int
        size: int

    class Output(Schema):
        courses: List[Any]  # `items` is a default attribute
        total: int
        page: int
        per_page: int
        links: dict

    items_attribute: str = "courses"

    def resolve_links(self, pagination: Input, total: int):
        return resolve_links(pagination, total, self.items_attribute)

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        size = pagination.size
        total = queryset.count()
        return {
            'courses': queryset[(page - 1) * size: page * size],
            'total': total,
            'page': page,
            'per_page': size,
            'links': {
                **self.resolve_links(pagination, total)
            }
        }


class EmployeePagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        page: int
        size: int

    class Output(Schema):
        employees: List[Any]  # `items` is a default attribute
        total: int
        page: int
        per_page: int
        links: dict

    items_attribute: str = "employees"

    def resolve_links(self, pagination: Input, total: int):
        return resolve_links(pagination, total, self.items_attribute)

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        size = pagination.size
        total = queryset.count()
        return {
            'employees': queryset[(page - 1) * size: page * size],
            'total': total,
            'page': page,
            'per_page': size,
            'links': {
                **self.resolve_links(pagination, total)
            }
        }

