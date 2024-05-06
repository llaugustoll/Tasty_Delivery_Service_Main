from enum import Enum


class OrderStatus(Enum):
    RECEBIDO = 1
    EM_PREPARACAO = 2
    PRONTO = 3
    FINALIZADO = 4
