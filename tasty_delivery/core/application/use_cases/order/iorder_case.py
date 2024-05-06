from abc import abstractmethod

from core.application.use_cases.ibase_use_case import IBaseUseCase


class IOrderCase(IBaseUseCase):
    @abstractmethod
    def get_by_client(self, client_id):
        raise NotImplementedError

    @abstractmethod
    def update_status(self, id: int, status: str):
        raise NotImplementedError
