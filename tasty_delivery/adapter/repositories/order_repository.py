from typing import List

from sqlalchemy.exc import IntegrityError

from adapter.database.models.order import Order as OrderDb
from adapter.database.models.order_product_association import OrderProductAssociation
from core.domain.repositories.iorder_repository import IOrderRepository


class OrderRepository(IOrderRepository):

    def __init__(self, db=None):
        self.db = db

    def get_all(self) -> List[OrderDb]:
        result = self.db.query(OrderDb).all()
        return result

    def get_by_id(self, id) -> OrderDb:
        return self.db.query(OrderDb).filter(OrderDb.id == id).scalar()

    def get_by_client(self, client_id) -> List[OrderDb]:
        return self.db.query(OrderDb).filter(OrderDb.client_id == client_id).all()

    def create(self, obj: List[OrderProductAssociation]):
        try:
            self.db.add_all(obj)
            self.db.flush()
            # self.db.refresh(obj)
            self.db.commit()
        except IntegrityError as err:
            raise err
        except Exception as e:
            raise e
        return obj

    def update(self, id, new_values):
        self.db.query(OrderDb).filter(OrderDb.id == id).update(new_values)
        self.db.flush()
        self.db.commit()
        return self.get_by_id(id)

    def delete(self, id):
        order = self.db.query(OrderDb).filter(OrderDb.id == id).scalar()
        if order:
            self.db.delete(order)
            self.db.commit()
        return None

    def update_status(self, id, status):
        self.db.query(OrderDb).filter(OrderDb.id == id).update(status)
        self.db.flush()
        self.db.commit()
        return self.get_by_id(id)
