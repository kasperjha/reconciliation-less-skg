from pydantic import BaseModel

from app.repository.collections import CollectionsRepository
from app.repository.datasets import DatasetsRepository
from app.services.algorithms import MeanStdQuantiser
from app.services.randomness import NistRandomnessAnalyser


class AnalysisOptions(BaseModel):
    collection_id: int


class AnalysisService:
    # TODO: shorten class names to CollectionsRepo and DatasetsRepo
    def __init__(self, collections: CollectionsRepository, datasets: DatasetsRepository):
        self.collections = collections
        self.datasets = datasets
        self.quantiser = MeanStdQuantiser()
        self.randomness = NistRandomnessAnalyser()

    def analyse_collection(self, options: AnalysisOptions):
        collection = self.collections.get_by_id(options.collection_id)
        filenames = [dataset.filename for dataset in collection.datasets]

        for filename in filenames:

            print("dataset:", filename)

            gateway, node = self.datasets.get(options.collection_id, filename)
            gw_quantised = self.quantiser.quantise(gateway)
            gw_randomeness = self.randomness.analyse_key_randomness(gw_quantised)

            print("gw_random?:", gw_randomeness)

            node_quantised = self.quantiser.quantise(node)
            node_randomness = self.randomness.analyse_key_randomness(node_quantised)

            print("node_random?:", node_randomness)
