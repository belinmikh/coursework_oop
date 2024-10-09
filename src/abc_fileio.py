from abc import ABC, abstractmethod


class FileManager(ABC):
    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def remove(self, n: int):
        pass

    def sort(self, reverse: bool = True):
        pass

    @abstractmethod
    def filter(self):
        pass

    @abstractmethod
    def clear(self):
        pass
