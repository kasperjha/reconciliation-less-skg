from pydantic import BaseModel
from app.repository.collections import CollectionsRepository
from app.repository.datasets import DatasetsRepository
from app.services.algorithms import MeanStdQuantiser
from app.services.randomness import NistRandomnessAnalyser, RandomnessResult


# class RandomnessTestResult(BaseModel):
#     test: str
#     passed: bool
#     p_value: float


# class RandomnessAnalysisResult(BaseModel):
#     tests_total: int
#     tests_passed: int
#     results: list[RandomnessTestResult]


class NoDatasetsError(Exception):
    pass


class AnalysisResultSamples(BaseModel):
    samples_raw: list[int]
    samples_processed: list[int]
    secret_key: str
    randomness: list[RandomnessResult]


class AnalysisResultDataset(BaseModel):
    filename: str
    gateway: AnalysisResultSamples
    node: AnalysisResultSamples


class AnalysisResultCollection(BaseModel):
    results: list[AnalysisResultDataset]


class AnalysisService:
    # TODO: shorten class names to CollectionsRepo and DatasetsRepo
    def __init__(self, collections: CollectionsRepository, datasets: DatasetsRepository):
        self.collections = collections
        self.datasets = datasets
        self.quantiser = MeanStdQuantiser()
        self.randomness = NistRandomnessAnalyser()

    def _analyse_samples(self, raw_samples: list[int]):
        samples_processed = raw_samples  # TODO: implement preprocessing
        samples_quantised = self.quantiser.quantise(samples_processed)
        results = {
            "samples_raw": raw_samples,
            "samples_processed": samples_processed,
            "secret_key": samples_quantised,
            "randomness": self.randomness.analyse_key_randomness(samples_quantised),
        }
        return AnalysisResultSamples(**results)

    def _analyse_dataset(self, id, filename: str):
        gateway, node = self.datasets.get(id, filename)
        results = {
            "filename": filename,
            "gateway": self._analyse_samples(gateway),
            "node": self._analyse_samples(node),
        }
        return AnalysisResultDataset(**results)

    def analyse_collection(self, id: int):
        collection = self.collections.get_by_id(id)
        filenames = [dataset.filename for dataset in collection.datasets]

        if not collection.datasets:
            raise NoDatasetsError()

        results = []
        for filename in filenames:
            results.append(self._analyse_dataset(id, filename))

        return AnalysisResultCollection(**{"results": results})
