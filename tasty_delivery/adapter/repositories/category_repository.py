from typing import List

from sqlalchemy.exc import IntegrityError

from adapter.database.models.category import Category as CategoryDb
from core.domain.repositories.icategory_repository import ICategoryRepository


class CategoryRepository(ICategoryRepository):

    def __init__(self, db=None):
        self.db = db

    def get_all(self) -> List[CategoryDb]:
        result = self.db.query(CategoryDb).filter(CategoryDb.is_deleted == False).all()
        return result

    def get_by_id(self, id) -> CategoryDb:
        return self.db.query(CategoryDb).filter(CategoryDb.id == id).scalar()

    def create(self, obj: CategoryDb) -> CategoryDb:
        try:
            self.db.add(obj)
            self.db.flush()
            self.db.refresh(obj)
            self.db.commit()
        except IntegrityError as err:
            raise err
        return obj

    def update(self, id, new_values):
        self.db.query(CategoryDb).filter(CategoryDb.id == id).update(new_values)
        self.db.flush()
        self.db.commit()
        return self.get_by_id(id)

    def delete(self, id, current_user):
        self.db.query(CategoryDb).filter(CategoryDb.id == id).update(
            {'is_deleted': True, 'updated_by': str(current_user.id)})
        self.db.flush()
        self.db.commit()
        return None
