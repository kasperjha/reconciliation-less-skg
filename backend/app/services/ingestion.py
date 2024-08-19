from fastapi import UploadFile

from app.repository.collections import CollectionsRepository
from app.repository.datasets import DatasetsRepository


class IngestionService:
    def __init__(self, collections: CollectionsRepository, datasets: DatasetsRepository):
        self.collections_repo = collections
        self.datasets_repo = datasets

    def ingest_dataset(self, collection_id: int, file: UploadFile):
        collection = self.collections_repo.get_by_id(collection_id)
        self.datasets_repo.create(collection.id, file)
        return self.collections_repo.update_dataset(collection_id, file.filename)
