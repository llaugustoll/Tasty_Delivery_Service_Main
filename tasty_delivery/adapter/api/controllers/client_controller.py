from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from adapter.database.db import get_db
from core.application.use_cases.client.client_case import ClientCase
from core.domain.entities.client import Client, ClientUpdate
from core.domain.exceptions.exception_schema import ObjectNotFound, ObjectDuplicated
from security.base import get_current_user


class ClientController:

    def __init__(self, client_case: ClientCase = None):
        self.router = APIRouter(
            tags=["Clients"],
            prefix='/clients'
        )
        self.router.add_api_route(
            path="/",
            endpoint=self.clients,
            methods=["GET"],
            response_model=List[Client],
            status_code=200,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.client_by_id,
            methods=["GET"],
            response_model=Client,
            responses={
                200: {"model": Client},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=200,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/cpf/{cpf}",
            endpoint=self.client_by_cpf,
            methods=["GET"],
            response_model=Client,
            responses={
                200: {"model": Client},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=200,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.update,
            methods=["PUT"],
            response_model=Client,
            responses={
                200: {"model": Client},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=200,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.delete,
            methods=["DELETE"],
            response_model=None,
            responses={
                204: {"model": None},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=204,
            response_model_exclude_none=True
        )

        self._client_case = client_case

    async def clients(self, db=Depends(get_db), current_user=Depends(get_current_user)):
        """
        Lista todos os clientes
        * Necessário permissionamento de usuário
        """
        return self._client_case(db, current_user=current_user).get_all()

    async def client_by_cpf(self, cpf: str, db=Depends(get_db), current_user=Depends(get_current_user)):
        """
        Lista clientes por CPF
        * Necessário permissionamento de usuário
        """
        return self._client_case(db, current_user=current_user).get_by_cpf(cpf)

    async def client_by_id(self, id: UUID, db=Depends(get_db), current_user=Depends(get_current_user)):
        """
        Lista cliente por {id}
        * Necessario permissionamento de usuário
        """
        return self._client_case(db, current_user=current_user).get_by_id(id)

    async def update(self, id: UUID, client: ClientUpdate, db=Depends(get_db), current_user=Depends(get_current_user)):
        """
        Atualiza cliente
        * Necessario permissionamento de usuário
        """
        return self._client_case(db, current_user=current_user).update(id, client)

    async def delete(self, id: UUID, db=Depends(get_db), current_user=Depends(get_current_user)):
        """
        Deleta cliente
        * Necessario permissionamento de usuário
        """
        self._client_case(db, current_user=current_user).delete(id)
