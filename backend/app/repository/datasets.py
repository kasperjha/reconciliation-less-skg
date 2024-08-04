from pathlib import Path

from fastapi import UploadFile


class MissingFilenameError(ValueError):
    pass


class DatasetsRepository:
    def __init__(self, dataset_dir="datasets"):
        self.dataset_dir = Path(dataset_dir)
        if not self.dataset_dir.exists():
            raise FileNotFoundError("Datasets folder does not exist.")

    def create(self, collection_id: int, file: UploadFile):
        """Persists a dataset at the local file system."""
        if file.filename is None:
            raise MissingFilenameError()

        # make sure collection and directory exists
        collection_dataset_dir = self.dataset_dir.joinpath(str(collection_id))
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

    def get(self, collection_id: int, filename: str):
        pass
