from ninja import Schema


class ErrorSchema(Schema):
    message: str = "model probablement supprimé ou inexistant"
