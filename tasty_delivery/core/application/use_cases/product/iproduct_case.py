from abc import abstractmethod

from core.application.use_cases.ibase_use_case import IBaseUseCase


class IProductCase(IBaseUseCase):

    @abstractmethod
    def get_by_category(self, category_id):
        raise NotImplementedError
