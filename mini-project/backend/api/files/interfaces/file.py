# files/interfaces/file.py

from abc import ABC, abstractmethod

class IFile(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def validation(self):
        pass

    @abstractmethod
    def analysis(self):
        pass

    @abstractmethod
    def output(self):
        pass