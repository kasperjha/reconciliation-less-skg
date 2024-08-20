from fastapi import APIRouter, HTTPException, UploadFile
from app.repository.collections import (
    Collection,
    CollectionCreate,
    CollectionNotFoundException,
    TestCollectionRepository,
)
from app.repository.datasets import DatasetsRepository, MissingFilenameError
from app.services.analysis import AnalysisResultCollection, AnalysisService, NoDatasetsError
from app.services.ingestion import IngestionService


router = APIRouter(prefix="/collections", tags=["collections"])


collections = TestCollectionRepository()
datasets = DatasetsRepository()


@router.get("/")
def get_collections():
    return collections.get_all()


@router.post("/")
def create_collection(collection: CollectionCreate) -> Collection:
    return collections.create(collection)


@router.get("/{id}")
def get_collection(id: int):
    try:
        collection = collections.get_by_id(id)
    except CollectionNotFoundException:
        raise HTTPException(404, "Collection not found.")
    return collection


@router.post("/{id}/analyse")
def analyse_collection_proto(id: int) -> AnalysisResultCollection:
    analysis = AnalysisService(collections, datasets)

    try:
        return analysis.analyse_collection(id)
    except NoDatasetsError:
        raise HTTPException(400, "No datasets in specified collection.")


@router.post("/{id}/datasets")
def upload_datasets(id: int, files: list[UploadFile]):
    ingestion = IngestionService(collections, datasets)

    try:
        for file in files:
            ingestion.ingest_dataset(id, file)
    except CollectionNotFoundException:
        raise HTTPException(404, "Collection not found")
    except MissingFilenameError:
        raise HTTPException(400, "A file is missing a filename")
    except FileExistsError:
        raise HTTPException(
            status_code=409,
            detail=f"Dataset named '{file.filename}' already exists for collection.",
        )

    return {"message": "Files processed sucessfully."}
