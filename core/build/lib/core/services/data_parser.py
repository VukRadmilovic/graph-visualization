from abc import abstractmethod, ABC
from core.model.graph import Graph


class DataParser(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def identifier(self) -> str:
        pass

    @abstractmethod
    def parse(self, data) -> Graph:
        pass
