from math import floor
from pydantic import BaseModel
from app.repository.collections import CollectionsRepository
from app.repository.datasets import DatasetsRepository
from app.services.algorithms import MeanStdQuantiser, Quantiser, SGPreprocessor, SchemeAnalyser, SchemeAnalysisResult
from app.services.randomness import NistRandomnessAnalyser, RandomnessResult


class NoDatasetsError(Exception):
    pass


class DatasetAnalysis(BaseModel):
    filename: str
    analysis: SchemeAnalysisResult


class AnalysisService:
    # TODO: shorten class names to CollectionsRepo and DatasetsRepo
    def __init__(self, collections: CollectionsRepository, datasets: DatasetsRepository):
        self.collections = collections
        self.datasets = datasets

    def _analyse_dataset(self, id, filename: str):
        # TODO: dependency injection for scheme analyser
        analyser = SchemeAnalyser(SGPreprocessor(), MeanStdQuantiser())
        gateway, node = self.datasets.get(id, filename)
        res = {"filename": filename, "analysis": analyser.analyse_key_material(node, gateway)}
        return DatasetAnalysis(**res)

    def analyse_collection(self, id: int) -> list[DatasetAnalysis]:
        collection = self.collections.get_by_id(id)
        filenames = [dataset.filename for dataset in collection.datasets]

        if not collection.datasets:
            raise NoDatasetsError()

        results = []
        for filename in filenames:
            results.append(self._analyse_dataset(id, filename))

        return results
