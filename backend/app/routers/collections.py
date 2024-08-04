from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel


# TODO: use a database
collections = []
collections.append(
    {"id": 1, "name": "Collection A", "datasets": [{"filename": "oliviera-car.csv"}]}
)  # type: ignore
collections.append({"id": 2, "name": "Collection B", "datasets": []})  # type: ignore


router = APIRouter(prefix="/collections", tags=["collections"])


class Dataset(BaseModel):
    filename: str


class CollectionCreate(BaseModel):
    name: str


class Collection(BaseModel):
    id: int
    name: str
    datasets: list[Dataset]


@router.get("/")
def get_collections() -> list[Collection]:
    return collections


@router.post("/collections/")
def create_collection(collection: CollectionCreate) -> Collection:
    newCollection: Collection = {
        "id": len(collections) + 1,
        "name": collection.name,
        "datasets": [],
    }  # type: ignore

    collections.append(newCollection)
    return newCollection


@router.get("/{collection_id}")
def get_collection(collection_id: int):
    collection = next(filter(lambda c: c["id"] == collection_id, collections), None)

    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found.")

    return collection


@router.post("/{collection_id}/datasets")
def upload_datasets(collection_id: int, files: list[UploadFile]):
    collection = next(filter(lambda c: c["id"] == collection_id, collections), None)

    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found.")

    datasets = Path("datasets")
    for file in files:
        if file.filename is None:
            raise HTTPException(status_code=400, detail="File without filename.")

        if datasets.joinpath(file.filename).exists():
            raise HTTPException(
                status_code=409,
                detail=f"Dataset with name '{file.filename}' already exists.",
            )

        # TODO: validate the format of the dataset

    for dataset in files:
        filename = dataset.filename
        assert filename is not None
        with open(datasets.joinpath(filename), "wb") as file:
            content = dataset.file.read()
            file.write(content)

    datasets = [{"filename": file.filename} for file in files]
    collection["datasets"].extend(datasets)

    return {"message": "Files processed sucessfully."}
