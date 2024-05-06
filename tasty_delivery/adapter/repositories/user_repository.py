from typing import List

from sqlalchemy.exc import IntegrityError

from adapter.database.models.user import User as UserDb
from core.domain.repositories.iuser_repository import IUserRepository


class UserRepository(IUserRepository):

    def __init__(self, db=None):
        self.db = db

    def get_all(self) -> List[UserDb]:
        result = self.db.query(UserDb).filter(UserDb.is_deleted == False, UserDb.is_active == True).all()
        return result

    def get_by_id(self, id) -> UserDb:
        return self.db.query(UserDb).filter(UserDb.id == id).scalar()

    def create(self, obj: UserDb) -> UserDb:
        try:
            self.db.add(obj)
            self.db.flush()
            self.db.refresh(obj)
            self.db.commit()
        except IntegrityError as err:
            raise err
        return obj

    def update(self, id, new_values):
        self.db.query(UserDb).filter(UserDb.id == id).update(new_values)
        self.db.flush()
        self.db.commit()
        return self.get_by_id(id)

    def delete(self, id, current_user):
        self.db.query(UserDb).filter(UserDb.id == id).update({'is_deleted': True, 'updated_by': str(current_user.id)})
        self.db.flush()
        self.db.commit()
        return None

    def get_by_username(self, username: str):
        return self.db.query(UserDb).filter(UserDb.username == username).scalar()

    def get_by_cpf(self, cpf):
        return self.db.query(UserDb).filter(UserDb.cpf == cpf).scalar()
