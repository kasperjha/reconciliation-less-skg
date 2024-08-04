from pathlib import Path
from fastapi import UploadFile

from app.repository.collections import CollectionsRepository


class MissingFilenameError(ValueError):
    pass


class IngestionService:
    def __init__(self, collections_repo: CollectionsRepository, dataset_dir="datasets"):
        self.collections_repo = collections_repo
        self.dataset_dir = Path(dataset_dir)

    def ingest_dataset(self, collection_id: int, file: UploadFile):

        if file.filename is None:
            raise MissingFilenameError()

        # make sure collection and directory exists
        collection = self.collections_repo.get_by_id(collection_id)
        collection_dataset_dir = self.dataset_dir.joinpath(str(collection.id))
        collection_dataset_dir.mkdir(exist_ok=True)

        # make sure datset name is unique for collection
        new_path = collection_dataset_dir.joinpath(file.filename)

        if new_path.exists():
            raise FileExistsError()

        # TODO: also validate that dataset has appropriate format

        # write to file system
        with open(new_path, "wb") as dstfile:
            content = file.file.read()  # TODO: chuck file upload for large files
            dstfile.write(content)

        return self.collections_repo.update_dataset(collection_id, file.filename)
