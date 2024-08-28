from abc import abstractmethod, ABC
from pydantic import BaseModel
from scipy.stats import pearsonr
from scipy.signal import savgol_filter


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


class Preprocessor(ABC):
    @abstractmethod
    def run(self, samples: list[int]) -> list[int]:
        pass


class SGPreprocessor(Preprocessor):
    def __init__(self, window_length=13, polyorder=3):
        self.window_length = window_length
        self.polyorder = polyorder

    def run(self, samples):
        return savgol_filter(samples, window_length=self.window_length, polyorder=self.polyorder)


class SchemeAnalysisResult(BaseModel):
    signal_correlation: float
    processed_correlation: float
    quantised_bdr: float


class SchemeAnalyser:

    def __init__(self, preprocessor: Preprocessor, quantiser: Quantiser):
        self.preprocessor = preprocessor
        self.quantiser = quantiser

    def _bit_disagreement_rate(self, key_node, key_gw) -> float:
        assert len(key_gw) == len(key_node)
        mismatch = 0
        for i in range(len(key_node)):
            mismatch += 0 if key_node[i] == key_gw[i] else 1
        return mismatch / len(key_node)

    def analyse_key_material(self, samples_node: list[int], samples_gw: list[int]):

        results = {}

        # calculate correlation coefficient on preliminary key material
        results["signal_correlation"] = pearsonr(x=samples_node, y=samples_gw).statistic

        # apply preprocessing step
        processed_node = self.preprocessor.run(samples_node)
        processed_gw = self.preprocessor.run(samples_gw)

        # recalculate correlation after processing
        results["processed_correlation"] = pearsonr(x=processed_node, y=processed_gw).statistic

        # apply quantisation step
        quantised_node = self.quantiser.quantise(samples_node)
        quantised_gw = self.quantiser.quantise(samples_gw)

        # calculate key material BD
        results["quantised_bdr"] = self._bit_disagreement_rate(quantised_node, quantised_gw)

        return SchemeAnalysisResult(**results)
