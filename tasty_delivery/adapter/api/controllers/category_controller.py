from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from adapter.database.db import get_db
from core.application.use_cases.category.category_case import CategoryCase
from core.domain.entities.category import CategoryIN, CategoryOUT
from core.domain.exceptions.exception_schema import ObjectNotFound, ObjectDuplicated
from security.base import get_current_user


class CategoryController:

    def __init__(self, category_case: CategoryCase = None):
        self.router = APIRouter(tags=["Categories"], prefix='/categories')
        self.router.add_api_route(
            path="/",
            endpoint=self.categories,
            methods=["GET"],
            response_model=List[CategoryOUT],
            status_code=200
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.category_by_id,
            methods=["GET"],
            response_model=CategoryOUT,
            responses={
                200: {"model": CategoryOUT},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=200
        )
        self.router.add_api_route(
            path="/",
            endpoint=self.create,
            methods=["POST"],
            response_model=CategoryOUT,
            responses={
                201: {"model": CategoryOUT},
                409: {"model": ObjectDuplicated}
            },
            status_code=201
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.update,
            methods=["PUT"],
            response_model=CategoryOUT,
            responses={
                200: {"model": CategoryOUT},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=200
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
            status_code=204
        )

        self._category_case = category_case

    async def categories(self):
        """
        Lista todas as categorias de produtos
        """
        return self._category_case().get_all()

    async def category_by_id(self, id: UUID,current_user=Depends(get_current_user)):
        """
        Lista categoria por {id} de produtos
        * Necessário permissionamento de usuário
        """
        return self._category_case(current_user).get_by_id(id)

    async def create(self, category: CategoryIN, current_user=Depends(get_current_user)):
        """
        Cria uma nova categoria
        * Necessário permissionamento de usuário
        """
        return self._category_case(current_user).create(category)

    async def update(self, id: UUID, category: CategoryIN, current_user=Depends(get_current_user)):
        """
        Atualiiza uma categoria
        * Necessário permissionamento de usuário
        """
        return self._category_case(current_user).update(id, category)

    async def delete(self, id: UUID, current_user=Depends(get_current_user)):
        """
        Delete uma categoria
        * Necessário permissionamento de usuário
        """
        self._category_case(current_user).delete(id)
        return None
