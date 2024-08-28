from fastapi import UploadFile
from pydantic import BaseModel


class CollectionDataset(BaseModel):
    filename: str


class Collection(BaseModel):
    id: int
    name: str
    datasets: list[CollectionDataset]


class CollectionCreate(BaseModel):
    name: str


class CollectionNotFoundException(Exception):
    pass


def save_dataset_to_disk(dataset: UploadFile):
    pass


class CollectionsRepository:
    def __init__(self):
        # TODO: separate test data from production data
        # TODO: store data in a persistant data store
        self.collections: list[Collection] = []

    def _get_dataset(self, collection: Collection, filename: str):
        def matches_filename(dataset: CollectionDataset):
            return dataset.filename == filename

        dataset = next(filter(matches_filename, collection.datasets), None)
        return dataset

    def get_all(self) -> list[Collection]:
        return self.collections

    def create(self, collection: CollectionCreate) -> Collection:
        newCollection = Collection(**{"id": len(self.collections), "name": collection.name, "datasets": []})
        self.collections.append(newCollection)
        return newCollection

    def get_by_id(self, id: int) -> Collection:
        collection = next(filter(lambda c: c.id == id, self.collections), None)
        if collection is None:
            raise CollectionNotFoundException()
        return collection

    def update_dataset(self, id: int, filename: str):
        """Associates collection with a dataset file."""
        collection = self.get_by_id(id)
        if collection is None:
            raise CollectionNotFoundException()

        # return existing if it exists
        dataset = self._get_dataset(collection, filename)
        if dataset is not None:
            return dataset

        dataset = CollectionDataset(**{"filename": filename})
        collection.datasets.append(dataset)
        return dataset
