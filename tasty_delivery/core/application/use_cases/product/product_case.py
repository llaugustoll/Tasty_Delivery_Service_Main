from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from adapter.database.models.user import User as UserDB
from core.application.use_cases.product.iproduct_case import IProductCase
from core.domain.entities.product import ProductIN, ProductOUT, ProductUpdateIN
from core.domain.exceptions.exception import DuplicateObject, ObjectNotFound
from logger import logger
from security.base import has_permission

import json
import requests
import os


class ProductCase(IProductCase):

    def __init__(self, current_user: UserDB = None):
        self.current_user = current_user

    def get_all(self):
        url = f"{os.environ['HOST_API_PRODUTO']}/products_api/"
        method = "get"
        return self.requisition(url , method)

    def get_by_id(self, id):
        url = f"{os.environ['HOST_API_PRODUTO']}/products_api/{id}"
        method = "get"
        return self.requisition(url , method)

    def get_by_category(self, category_id):
        url = f"{os.environ['HOST_API_PRODUTO']}/products_api/categories/{category_id}"
        method = "get"
        return self.requisition(url , method)
    
    @has_permission(permission=['admin'])
    def create(self, obj: ProductIN) -> ProductOUT:
        data = {
            "name": obj.name ,
            "description": obj.description,
            "price": obj.price,
            "category_id": obj.category_id,
            "created_by": self.current_user.name
        }

        url = f"{os.environ['HOST_API_PRODUTO']}/products_api/"
        method = "post"

        return self.requisition(url,method,json.dumps(data))

    @has_permission(permission=['admin'])
    def update(self, id, new_values: ProductUpdateIN) -> ProductOUT:
        data = {
            "name": new_values.name ,
            "description": new_values.description,
            "price": new_values.price,
            "category_id": new_values.category_id,
            "created_by": self.current_user.name
        }

        url = f"{os.environ['HOST_API_PRODUTO']}/products_api/{id}"
        method = "put"
        return self.requisition(url,method,json.dumps(data))

    @has_permission(permission=['admin'])
    def delete(self, id):
        created_by = self.current_user.name
        url = f"{os.environ['HOST_API_PRODUTO']}/products_api/{id}/{created_by}"
        method = "delete"
        return self.requisition(url,method)

    def requisition(self,url,method, data = None):
        if method == 'get':
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return {"erro": "Não foi possível acessar a API"}
        elif method == 'post':
            response = requests.post(url, data=data)
            if response.status_code == 201:
                return response.json()
            else:
                return {"erro": "Não foi possível acessar a API"}
        elif method == 'put':
            response = requests.put(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                return {"erro": "Não foi possível acessar a API"}
        elif method == 'delete':
            response = requests.delete(url)
            if response.status_code == 200:
                return response.json()
            else:
                return {"erro": "Não foi possível acessar a API"}

