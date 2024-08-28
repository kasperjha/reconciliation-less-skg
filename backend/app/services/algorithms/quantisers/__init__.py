from abc import abstractmethod, ABC


class Quantiser(ABC):
    @abstractmethod
    def run(self, samples: list[int]) -> str:
        pass
