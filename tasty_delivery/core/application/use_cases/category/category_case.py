from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from core.application.use_cases.category.icategory_case import ICategoryCase
from core.domain.entities.category import CategoryOUT
from core.domain.entities.user import User as UserDB
from core.domain.exceptions.exception import DuplicateObject, ObjectNotFound
from logger import logger
from security.base import has_permission

import json
import requests
import os

class CategoryCase(ICategoryCase):
    def __init__(self, current_user: UserDB = None):
        self.current_user = current_user

    def get_all(self):
        url = f"{os.environ['HOST_API_PRODUTO']}/categories_api/"
        method = "get"
        return self.requisition(url , method)

    @has_permission(permission=['admin'])
    def get_by_id(self, id):
        url = f"{os.environ['HOST_API_PRODUTO']}/categories_api/{id}"
        method = "get"
        return self.requisition(url , method)
    
    @has_permission(permission=['admin'])
    def create(self, obj: CategoryOUT) -> CategoryOUT:
        data = {
            "name": obj.name
        }

        url = f"{os.environ['HOST_API_PRODUTO']}/categories_api/"
        method = "post"

        return self.requisition(url,method,json.dumps(data))

    @has_permission(permission=['admin'])
    def update(self, id, new_values: CategoryOUT) -> CategoryOUT:
        data = {
            "name": new_values.name
        }

        url = f"{os.environ['HOST_API_PRODUTO']}/categories_api/{id})"
        method = "put"
        return self.requisition(url,method,json.dumps(data))

    @has_permission(permission=['admin'])
    def delete(self, id):
        created_by = self.current_user.name
        url = f"{os.environ['HOST_API_PRODUTO']}/categories_api/{id}/{created_by}"
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