from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from security.base import get_current_user
from adapter.database.db import get_db
from core.application.use_cases.user.user_case import UserCase
from core.domain.entities.user import User as User, UserUpdate, UserOUT
from core.domain.exceptions.exception_schema import ObjectNotFound, ObjectDuplicated


class UserController:

    def __init__(self, user_case: UserCase = None):
        self.router = APIRouter(
            tags=["Users"],
            prefix='/users',
            dependencies=[Depends(get_current_user)]
        )
        self.router.add_api_route(
            path="/",
            endpoint=self.users,
            methods=["GET"],
            response_model=List[User],
            status_code=200,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.user_by_id,
            methods=["GET"],
            response_model=User,
            responses={
                200: {"model": User},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=200,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/",
            endpoint=self.create,
            methods=["POST"],
            response_model=UserOUT,
            response_model_by_alias=True,
            responses={
                201: {"model": UserOUT},
                409: {"model": ObjectDuplicated}
            },
            status_code=201,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.update,
            methods=["PUT"],
            response_model=User,
            responses={
                200: {"model": User},
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

        self._user_case = user_case

    async def users(self, db=Depends(get_db), current_user=Depends(get_current_user)):
        """
        Lista todos os usuários
        * Necessário ter permissionamento de usuário admin
        """
        return self._user_case(db).get_all()

    async def user_by_id(self, id: UUID, db=Depends(get_db), current_user=Depends(get_current_user)):
        """
        Lista todos os usuários por {id}
        * Necessário ter permissionamento de usuário admin
        """
        return self._user_case(db).get_by_id(id)

    async def create(self, user: User, db=Depends(get_db), current_user=Depends(get_current_user)):
        """
        Cria usuário
        * Necessário ter permissionamento de usuário admin
        """
        return self._user_case(db, current_user).create(user)

    async def update(self, id: UUID, user: UserUpdate, db=Depends(get_db), current_user=Depends(get_current_user)):
        """
        Cria usuário
        * Necessário ter permissionamento de usuário admin
        """
        return self._user_case(db, current_user).update(id, user)

    async def delete(self, id: UUID, db=Depends(get_db), current_user=Depends(get_current_user)):
        """
        Deleta usuário
        * Necessário ter permissionamento de usuário admin
        """
        self._user_case(db, current_user).delete(id)
