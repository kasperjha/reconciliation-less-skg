from abc import abstractmethod, ABC


class Preprocessor(ABC):
    @abstractmethod
    def run(self, samples: list[int]) -> list[int]:
        pass
