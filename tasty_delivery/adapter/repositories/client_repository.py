from typing import List

from sqlalchemy.exc import IntegrityError

from adapter.database.models.client import Client as ClientDb
from core.domain.repositories.iclient_repository import IClientRepository


class ClientRepository(IClientRepository):

    def __init__(self, db=None):
        self.db = db

    def get_all(self) -> List[ClientDb]:
        result = self.db.query(ClientDb).filter(ClientDb.is_deleted == False, ClientDb.is_active == True).all()
        return result

    def get_by_id(self, id) -> ClientDb:
        return self.db.query(ClientDb).filter(ClientDb.id == id).scalar()

    def create(self, obj: ClientDb) -> ClientDb:
        try:
            self.db.add(obj)
            self.db.flush()
            self.db.refresh(obj)
            self.db.commit()
        except IntegrityError as err:
            raise err
        return obj

    def update(self, id, new_values):
        self.db.query(ClientDb).filter(ClientDb.id == id).update(new_values)
        self.db.flush()
        self.db.commit()
        return self.get_by_id(id)

    def delete(self, id, current_user):
        self.db.query(ClientDb).filter(ClientDb.id == id).update(
            {'is_deleted': True, 'updated_by': str(current_user.id)})
        self.db.flush()
        self.db.commit()
        return None

    def get_by_username(self, username: str):
        return self.db.query(ClientDb).filter(ClientDb.username == username).scalar()

    def get_by_cpf(self, cpf):
        return self.db.query(ClientDb).filter(ClientDb.cpf == cpf).scalar()
