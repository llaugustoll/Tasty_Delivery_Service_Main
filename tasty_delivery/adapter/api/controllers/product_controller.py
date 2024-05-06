from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from adapter.database.db import get_db
from core.application.use_cases.product.product_case import ProductCase
from core.domain.entities.product import ProductOUT, ProductIN, ProductUpdateIN
from core.domain.exceptions.exception_schema import ObjectNotFound, ObjectDuplicated
from security.base import get_current_user

import requests


class ProductController:

    def __init__(self, product_case: ProductCase = None):
        self.router = APIRouter(tags=["Products"], prefix='/products')
        self.router.add_api_route(
            path="/",
            endpoint=self.products,
            methods=["GET"],
            response_model=List[ProductOUT],
            status_code=200
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.product_by_id,
            methods=["GET"],
            response_model=ProductOUT,
            responses={
                200: {"model": ProductOUT},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=200
        )
        self.router.add_api_route(
            path="/categories/{category_id}",
            endpoint=self.products_by_category,
            methods=["GET"],
            response_model=List[ProductOUT],
            status_code=200
        )
        self.router.add_api_route(
            path="/",
            endpoint=self.create,
            methods=["POST"],
            response_model=ProductOUT,
            responses={
                201: {"model": ProductOUT},
                409: {"model": ObjectDuplicated}
            },
            status_code=201
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.update,
            methods=["PUT"],
            response_model=ProductOUT,
            responses={
                200: {"model": ProductOUT},
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
            status_code=200
        )

        self._product_case = product_case

    async def products(self, db=Depends(get_db)):
        """
        Retorna todos os produtos cadastrados
        """

        url = "http://tasty_delivery_msvc_product:8000/products2/"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return {"erro": "Não foi possível acessar a API"}


        # return self._product_case(db).get_all()

    async def product_by_id(self, id: UUID, db=Depends(get_db)):
        """
        Retorna produto por id
        """
        return self._product_case(db).get_by_id(id)

    async def products_by_category(self, category_id: UUID, db=Depends(get_db)):
        """
        Retorna produtos por categoria
        """
        return self._product_case(db).get_by_category(category_id)

    async def create(self, product: ProductIN, db=Depends(get_db), current_user=Depends(get_current_user)):
        """
        Cadastra produto
        * Necessário permissionamento de usuário admin
        """
        return self._product_case(db, current_user).create(product)

    async def update(self, id: UUID, product: ProductUpdateIN, db=Depends(get_db),
                     current_user=Depends(get_current_user)):
        """
        Atualiza produto
        * Necessário permissionamento de usuário admin
        """
        return self._product_case(db, current_user).update(id, product)

    async def delete(self, id: UUID, db=Depends(get_db), current_user=Depends(get_current_user)):
        """
        Deleta produto
        * Necessário permissionamento de usuário admin
        """
        return self._product_case(db, current_user).delete(id)
