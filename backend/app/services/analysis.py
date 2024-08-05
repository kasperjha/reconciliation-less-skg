from pydantic import BaseModel

from app.repository.collections import CollectionsRepository
from app.repository.datasets import DatasetsRepository
from app.services.algorithms import MeanStdQuantiser


class AnalysisOptions(BaseModel):
    collection_id: int


class AnalysisService:
    # TODO: shorten class names to CollectionsRepo and DatasetsRepo
    def __init__(self, collections: CollectionsRepository, datasets: DatasetsRepository):
        self.collections = collections
        self.datasets = datasets
        self.quantiser = MeanStdQuantiser()

    def analyse_collection(self, options: AnalysisOptions):
        collection = self.collections.get_by_id(options.collection_id)
        filenames = [dataset.filename for dataset in collection.datasets]

        for filename in filenames:
            gateway, node = self.datasets.get(options.collection_id, filename)
            quantised_gateway = self.quantiser.quantise(gateway)
            quantised_node = self.quantiser.quantise(node)

            raise NotImplementedError()
