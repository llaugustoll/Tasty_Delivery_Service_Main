from abc import abstractmethod

from core.domain.repositories.ibase_repository import IBaseRepository


class IOrderRepository(IBaseRepository):

    @abstractmethod
    def get_by_client(self, client_id):
        raise NotImplementedError

    @abstractmethod
    def update_status(self, id, status):
        raise NotImplementedError
