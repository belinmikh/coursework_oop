from abc import ABC, abstractmethod


class BaseModel(ABC):
    @staticmethod
    @abstractmethod
    def from_dict(data: dict):
        pass
