from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from adapter.database.models.product import Product as ProductDB
from adapter.repositories.product_repository import ProductRepository
from adapter.database.models.user import User as UserDB
from core.application.use_cases.product.iproduct_case import IProductCase
from core.domain.entities.product import ProductIN, ProductOUT, ProductUpdateIN
from core.domain.exceptions.exception import DuplicateObject, ObjectNotFound
from logger import logger
from security.base import has_permission


class ProductCase(IProductCase):

    def __init__(self, db=None, current_user: UserDB = None):
        self.repository = ProductRepository(db)
        self.current_user = current_user

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        result = self.repository.get_by_id(id)
        if not result:
            msg = f"Produto {id} não encontrado"
            logger.warning(msg)
            raise ObjectNotFound(msg, 404)
        return result

    def get_by_category(self, category_id):
        return self.repository.get_by_category(category_id)

    @has_permission(permission=['admin'])
    def create(self, obj: ProductIN) -> ProductOUT:
        try:
            id = uuid4()
            return self.repository.create(ProductDB(
                **obj.model_dump(exclude_none=True),
                id=id,
                created_by=self.current_user.id)
            )
        except IntegrityError:
            msg = "Produto já existente na base de dados"
            logger.warning(msg)
            raise DuplicateObject(msg, 409)

    @has_permission(permission=['admin'])
    def update(self, id, new_values: ProductUpdateIN) -> ProductOUT:
        new_values = new_values.model_dump(exclude_none=True)
        new_values['updated_by'] = self.current_user.id
        return self.repository.update(id, new_values)

    @has_permission(permission=['admin'])
    def delete(self, id):
        return self.repository.delete(id, self.current_user)
