from abc import abstractmethod, ABC


def std_dev(samples):
    n = len(samples)
    mean = sum(samples) / n
    sumsq = sum(v * v for v in samples)
    return (sumsq / n - mean * mean) ** 0.5


class Quantiser(ABC):
    @abstractmethod
    def quantise(self, samples: list[int]) -> str:
        pass


class MeanStdQuantiser(Quantiser):
    def quantise(self, samples: list[int]) -> str:
        mean = sum(samples) / len(samples)
        std = std_dev(samples)
        alpha = 0
        threshold_pos = mean + alpha * std
        threshold_neg = mean - alpha * std

        bits = ""

        for sample in samples:
            if threshold_pos < sample:
                bits += "1"
            if sample < threshold_neg:
                bits += "0"
            else:
                continue

        return bits


class DifferentialQuantiser(Quantiser):
    def quantise(self, samples: list[int]) -> str:
        raise NotImplementedError()
