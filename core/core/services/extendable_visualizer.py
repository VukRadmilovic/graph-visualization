from core.model.graph import Graph
from abc import ABC, abstractmethod


class ExtendableVisualizer(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def identifier(self) -> str:
        pass

    @abstractmethod
    def bird_view(self, graph: Graph) -> str:
        pass

    @abstractmethod
    def main_view(self, graph: Graph) -> str:
        pass
