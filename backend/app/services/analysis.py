from pydantic import BaseModel
from app.repository.collections import CollectionsRepository
from app.repository.datasets import DatasetsRepository
from scipy.stats import pearsonr
from app.services.algorithms.preprocessors import Preprocessor
from app.services.algorithms.preprocessors.SavitzkyGolay import SavitzkyGolay
from app.services.algorithms.preprocessors.Kalman import Kalman
from app.services.algorithms.quantisers import Quantiser
from app.services.algorithms.quantisers.MeanStd import MeanStdQuantiser


class NoDatasetsError(Exception):
    pass


class UnknownPreprocessor(Exception):
    pass


class UnknownQuantiser(Exception):
    pass


class SchemeAnalysisResult(BaseModel):
    signal_correlation: float
    processed_correlation: float
    quantised_bdr: float


class SchemeAnalyser:

    def __init__(self):
        self.preprocessors = {}
        self.quantisers = {}

    def register_quantiser(self, name: str, quantiser: Quantiser):
        self.quantisers[name] = quantiser

    def list_quantisers(self):
        return self.quantisers.keys()

    def register_preprocessor(self, name: str, preprocessor: Preprocessor):
        self.preprocessors[name] = preprocessor

    def list_preprocessors(self):
        return self.preprocessors.keys()

    def _bit_disagreement_rate(self, key_node, key_gw) -> float:
        assert len(key_gw) == len(key_node)
        mismatch = 0
        for i in range(len(key_node)):
            mismatch += 0 if key_node[i] == key_gw[i] else 1
        return mismatch / len(key_node)

    def _execute(self, node: list[int], gw: list[int], preprocessor: Preprocessor, quantiser: Quantiser):
        results = {}

        # calculate correlation coefficient on preliminary key material
        results["signal_correlation"] = pearsonr(x=node, y=gw).statistic

        # apply preprocessing step
        processed_node = preprocessor.run(node)
        processed_gw = preprocessor.run(gw)

        # recalculate correlation after processing
        results["processed_correlation"] = pearsonr(x=processed_node, y=processed_gw).statistic

        # apply quantisation step
        quantised_node = quantiser.run(node)
        quantised_gw = quantiser.run(gw)

        # calculate key material BD
        results["quantised_bdr"] = self._bit_disagreement_rate(quantised_node, quantised_gw)

        return SchemeAnalysisResult(**results)

    def analyse_key_material(self, node: list[int], gw: list[int], preprocessor: str, quantiser: str):

        preprocessor = self.preprocessors[preprocessor]
        quantiser = self.quantisers[quantiser]

        if preprocessor is None:
            raise UnknownPreprocessor()

        if quantiser is None:
            raise UnknownQuantiser()

        return self._execute(node, gw, preprocessor, quantiser)


class DefaultAnalyser(SchemeAnalyser):
    def __init__(self):
        super().__init__()
        self.register_preprocessor("savgol", SavitzkyGolay())
        self.register_preprocessor("kalman", Kalman())
        self.register_quantiser("mean_std", MeanStdQuantiser())


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
        analyser = DefaultAnalyser()
        gateway, node = self.datasets.get(id, filename)

        # for q in ["combined_multilevel", "mean_std"]:
        #     analysis_result = analyser.analyse_key_material(node, gateway, "savgol", q)
        #     print(filename, q, analysis_result.quantised_bdr)

        res = {"filename": filename, "analysis": analyser.analyse_key_material(node, gateway, "kalman", "mean_std")}

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
