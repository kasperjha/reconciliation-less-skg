from pydantic import BaseModel
from app.repository.collections import CollectionsRepository
from app.repository.datasets import DatasetsRepository
from app.services.algorithms import MeanStdQuantiser
from app.services.randomness import NistRandomnessAnalyser, RandomnessResult


class NoDatasetsError(Exception):
    pass


class AnalysisResultDataset(BaseModel):
    mismatch_count: float
    filename: str
    randomness: list[RandomnessResult]
    key_length: int
    node_key: str
    gw_key: str
    secret_key: str | None


class AnalysisResultCollection(BaseModel):
    results: list[AnalysisResultDataset]


class AnalysisService:
    # TODO: shorten class names to CollectionsRepo and DatasetsRepo
    def __init__(self, collections: CollectionsRepository, datasets: DatasetsRepository):
        self.collections = collections
        self.datasets = datasets
        self.quantiser = MeanStdQuantiser()
        self.randomness = NistRandomnessAnalyser()

    def _get_key(self, raw_samples: list[int]):
        samples_processed = raw_samples  # TODO: implement preprocessing
        samples_quantised = self.quantiser.quantise(samples_processed)
        return samples_quantised

    def _get_mismatch_count(self, node_key, gw_key) -> float:
        same = 0
        for i in range(len(node_key)):
            same += 1 if node_key[i] == gw_key[i] else 0
        return same

    def _analyse_dataset(self, id, filename: str):
        gateway, node = self.datasets.get(id, filename)
        gateway_key = self._get_key(gateway)
        node_key = self._get_key(node)
        key_length = min(len(gateway_key), len(node_key))
        results = {
            "key_length": key_length,
            "mismatch_count": self._get_mismatch_count(node_key[:key_length], gateway_key[:key_length]),
            "filename": filename,
            "node_key": node_key[:key_length],
            "gw_key": gateway_key[:key_length],
            "secret_key": node_key[:key_length] if node_key == gateway_key else None,
            "randomness": self.randomness.analyse_key_randomness(node_key) if node_key == gateway_key else [],
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
