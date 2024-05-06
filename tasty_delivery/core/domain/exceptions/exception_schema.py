from pydantic import BaseModel, Field

OBJECT_NOT_FOUND_MESSAGE = "Objeto não encontrado"
OBJECT_DUPLICATED_MESSAGE = "Objeto duplicado na base de dados"


class DefaultResponse(BaseModel):
    def __init__(self):
        super(DefaultResponse, self).__init__()

    detail: str = Field(
        default="Problema de conexão com o banco de dados",
        title="Mensagem",
        description="Mensagem de erro ou descrição do retorno",
        example="Internal Server Error!"
    )


class ObjectNotFound(DefaultResponse):
    detail: str = Field(
        default=OBJECT_NOT_FOUND_MESSAGE,
        title="Mensagem",
        description=OBJECT_NOT_FOUND_MESSAGE,
        example=OBJECT_NOT_FOUND_MESSAGE
    )


class ObjectDuplicated(DefaultResponse):
    detail: str = Field(
        default=OBJECT_DUPLICATED_MESSAGE,
        title="Mensagem",
        description=OBJECT_DUPLICATED_MESSAGE,
        example=OBJECT_DUPLICATED_MESSAGE
    )
