from typing import List

from sqlalchemy.exc import IntegrityError

from adapter.database.models.product import Product as ProductDb
from core.domain.repositories.iproduct_repository import IProductRepository


class ProductRepository(IProductRepository):

    def __init__(self, db=None):
        self.db = db

    def get_all(self) -> List[ProductDb]:
        result = self.db.query(ProductDb).all()
        return result

    def get_by_id(self, id) -> ProductDb:
        return self.db.query(ProductDb).filter(ProductDb.id == id).scalar()

    def get_by_category(self, category_id) -> List[ProductDb]:
        return self.db.query(ProductDb).filter(ProductDb.category_id == category_id).all()

    def create(self, obj: ProductDb) -> ProductDb:
        try:
            self.db.add(obj)
            self.db.flush()
            self.db.refresh(obj)
            self.db.commit()
        except IntegrityError as err:
            raise err
        return obj

    def update(self, id, new_values):
        self.db.query(ProductDb).filter(ProductDb.id == id).update(new_values)
        self.db.flush()
        self.db.commit()
        return self.get_by_id(id)

    def delete(self, id, current_user):
        self.db.query(ProductDb).filter(ProductDb.id == id).update(
            {'is_deleted': True, 'updated_by': str(current_user.id)})
        self.db.flush()
        self.db.commit()
        return None
