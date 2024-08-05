from pydantic import BaseModel

from app.repository.collections import CollectionsRepository
from app.repository.datasets import DatasetsRepository


def std_dev(samples):
    n = len(samples)
    mean = sum(samples) / n
    sumsq = sum(v * v for v in samples)
    return (sumsq / n - mean * mean) ** 0.5


def mean_std_quantization(samples: list[int]):
    mean = sum(samples) / len(samples)
    std = std_dev(samples)
    alpha = 0
    threshold_pos = mean + alpha * std
    threshold_neg = mean - alpha * std

    bits: list[str] = []

    for sample in samples:
        if threshold_pos < sample:
            bits.append("1")
        if sample < threshold_neg:
            bits.append("0")
        else:
            continue

    return bits


def differential_quantization():
    raise NotImplementedError()


class AnalysisOptions(BaseModel):
    collection_id: int


class AnalysisService:
    # shorten class names to CollectionsRepo and DatasetsRepo
    def __init__(self, collections: CollectionsRepository, datasets: DatasetsRepository):
        self.collections = collections
        self.datasets = datasets

    def _evaluate_randomness(self, bits) -> float:
        raise NotImplementedError()

    def analyse_collection(self, options: AnalysisOptions):

        collection = self.collections.get_by_id(options.collection_id)
        filenames = [dataset.filename for dataset in collection.datasets]
        results = []

        for filename in filenames:
            gateway, node = self.datasets.get(options.collection_id, filename)
            quantised_gateway = mean_std_quantization(gateway)
            quantised_node = mean_std_quantization(node)

            randomness_gateway = self._evaluate_randomness(quantised_gateway)
            randomness_node = self._evaluate_randomness(quantised_node)

            raise NotImplementedError()
