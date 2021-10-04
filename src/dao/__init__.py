from abc import (
    ABCMeta,
    abstractmethod
)


# -----------------------------------------------------------------------------
# CLASS DAO
# -----------------------------------------------------------------------------
class DataAccessObject(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def query(self, match_criteria: dict) -> list:
        pass

    @abstractmethod
    def has(self, identifier: str, key: str) -> bool:
        pass

    @abstractmethod
    def get(self, identifier: str, key: str) -> dict or None:
        pass

    @abstractmethod
    def create(self, entity_state: dict) -> dict or None:
        pass

    @abstractmethod
    def update(self, entity_id: str, entity_state: dict) -> bool:
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        pass