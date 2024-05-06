from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from adapter.database.models.client import Client as ClientDB
from adapter.repositories.client_repository import ClientRepository
from core.application.use_cases.client.iclient_case import IClientCase
from core.domain.entities.client import Client, ClientUpdate
from core.domain.exceptions.exception import DuplicateObject, ObjectNotFound
from logger import logger
from security.base import has_permission


class ClientCase(IClientCase):

    def __init__(self, db=None, current_user=None):
        self.current_user = current_user
        self.repository = ClientRepository(db)

    @has_permission(permission=['admin'])
    def get_all(self):
        result = self.repository.get_all()
        return result

    @has_permission(permission=['admin'])
    def get_by_id(self, id):
        result = self.repository.get_by_id(id)
        if not result:
            msg = f"Cliente {id} não encontrado"
            logger.warning(msg)
            raise ObjectNotFound(msg, 404)
        return result

    @has_permission(permission=['admin', 'client'])
    def create(self, obj: Client) -> Client:
        try:
            obj.id = uuid4()
            obj.scopes.append('client')
            result = self.repository.create(ClientDB(**obj.model_dump(exclude_none=True)))
            return Client(**vars(result))
        except IntegrityError:
            msg = "Cliente já existente na base de dados"
            logger.warning(msg)
            raise DuplicateObject(msg, 409)
        except Exception as err:
            raise err

    @has_permission(permission=['admin'])
    def update(self, id, new_values: ClientUpdate) -> Client:
        return self.repository.update(id, new_values.model_dump(exclude_none=True))

    @has_permission(permission=['admin'])
    def delete(self, id):
        return self.repository.delete(id, self.current_user)

    @has_permission(permission=['admin', 'client'])
    def get_by_cpf(self, cpf):
        result = self.repository.get_by_cpf(cpf)
        if result:
            return Client(**vars(result))
        else:
            return None
