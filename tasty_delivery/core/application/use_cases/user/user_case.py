from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from adapter.database.models.user import User as UserDB
from adapter.repositories.user_repository import UserRepository
from core.application.use_cases.user.iuser_case import IUserCase
from core.domain.entities.user import User, UserOUT
from core.domain.exceptions.exception import DuplicateObject, ObjectNotFound
from logger import logger
from security.base import has_permission


class UserCase(IUserCase):

    def __init__(self, db=None, current_user=None):
        self.repository = UserRepository(db)
        self.current_user = current_user

    @has_permission(permission=['admin'])
    def get_all(self):
        return self.repository.get_all()

    @has_permission(permission=['admin'])
    def get_by_id(self, id):
        result = self.repository.get_by_id(id)
        if not result:
            msg = f"Usuário {id} não encontrado"
            logger.warning(msg)
            raise ObjectNotFound(msg, 404)
        return result

    @has_permission(permission=['admin'])
    def create(self, obj: User) -> UserOUT:

        try:
            obj.id = uuid4()
            obj.scopes.append('admin')
            result = self.repository.create(UserDB(**obj.model_dump(exclude_none=True, by_alias=True)))
            return UserOUT(**vars(result))
        except IntegrityError:
            msg = "Usuário já existente na base de dados"
            logger.warning(msg)
            raise DuplicateObject(msg, 409)

    @has_permission(permission=['admin'])
    def update(self, id, new_values: User) -> User:
        new_values.id = None
        return self.repository.update(id, new_values.model_dump(exclude_none=True))

    @has_permission(permission=['admin'])
    def delete(self, id):
        return self.repository.delete(id, self.current_user)

    @has_permission(permission=['admin', 'login'])
    def get_by_username(self, user_name: str):
        return self.repository.get_by_username(user_name)

    @has_permission(permission=['admin'])
    def get_by_cpf(self, cpf: str):
        return self.repository.get_by_cpf(cpf)
