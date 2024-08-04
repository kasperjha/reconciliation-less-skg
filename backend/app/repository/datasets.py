from pathlib import Path

from fastapi import UploadFile


class MissingFilenameError(ValueError):
    pass


class DatasetsRepository:
    def __init__(self, dataset_dir="datasets"):
        self.dataset_dir = Path(dataset_dir)
        if not self.dataset_dir.exists():
            raise FileNotFoundError("Datasets folder does not exist.")

    def _build_collection_dir(self, collection_id):
        return self.dataset_dir.joinpath(str(collection_id))

    def _build_dataset_path(self, collection_id, dataset_filename):
        return self._build_collection_dir(collection_id).joinpath(dataset_filename)

    def create(self, collection_id: int, file: UploadFile):
        """Persists a dataset at the local file system."""
        if file.filename is None:
            raise MissingFilenameError()

        # make sure collection and directory exists
        collection_dir = self._build_collection_dir()
        collection_dir.mkdir(exist_ok=True)

        # make sure datset name is unique for collection
        dataset_path = self._build_dataset_path()

        if dataset_path.exists():
            raise FileExistsError()

        # TODO: also validate that dataset has appropriate format

        # write to file system
        with open(dataset_path, "wb") as dstfile:
            content = file.file.read()  # TODO: chuck file upload for large files
            dstfile.write(content)

    def get(self, collection_id: int, filename: str):
        pass
