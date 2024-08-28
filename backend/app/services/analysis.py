from pydantic import BaseModel
from app.repository.collections import CollectionsRepository
from app.repository.datasets import DatasetsRepository
from scipy.stats import pearsonr
from app.services.algorithms.preprocessors import Preprocessor
from app.services.algorithms.preprocessors.SavitzkyGolay import SavitzkyGolay
from app.services.algorithms.quantisers import Quantiser
from app.services.algorithms.quantisers.MeanStd import MeanStdQuantiser


class NoDatasetsError(Exception):
    pass


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
        quantised_node = self.quantiser.run(samples_node)
        quantised_gw = self.quantiser.run(samples_gw)

        # calculate key material BD
        results["quantised_bdr"] = self._bit_disagreement_rate(quantised_node, quantised_gw)

        return SchemeAnalysisResult(**results)


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
        analyser = SchemeAnalyser(SavitzkyGolay(), MeanStdQuantiser())
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
