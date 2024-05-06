from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from adapter.database.models.category import Category as CategoryDB
from adapter.repositories.category_repository import CategoryRepository
from core.application.use_cases.category.icategory_case import ICategoryCase
from core.domain.entities.category import CategoryOUT
from core.domain.entities.user import User
from core.domain.exceptions.exception import DuplicateObject, ObjectNotFound
from logger import logger
from security.base import has_permission


class CategoryCase(ICategoryCase):

    def __init__(self, db=None, current_user: User = None):
        self.repository = CategoryRepository(db)
        self.current_user = current_user

    def get_all(self):
        result = self.repository.get_all()
        return result

    @has_permission(permission=['admin'])
    def get_by_id(self, id):
        result = self.repository.get_by_id(id)
        if not result:
            msg = f"Categoria {id} não encontrado"
            logger.warning(msg)
            raise ObjectNotFound(msg, 404)
        return result

    @has_permission(permission=['admin'])
    def create(self, obj: CategoryOUT) -> CategoryOUT:
        obj.id = uuid4()
        obj.created_by = self.current_user.id
        try:
            return self.repository.create(CategoryDB(**vars(obj)))
        except IntegrityError:
            msg = "Categoria já existente na base de dados"
            logger.warning(msg)
            raise DuplicateObject(msg, 409)

    @has_permission(permission=['admin'])
    def update(self, id, new_values: CategoryOUT) -> CategoryOUT:
        new_values.id = None
        new_values.updated_by = self.current_user.id
        return self.repository.update(id, new_values.model_dump(exclude_none=True))

    @has_permission(permission=['admin'])
    def delete(self, id):
        return self.repository.delete(id, self.current_user)
