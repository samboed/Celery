from bson import ObjectId
from gridfs import GridFS, GridOut
from pymongo import MongoClient

from src.config import MONGO_URL


mongo_client = MongoClient(
    MONGO_URL
)

mongo_database = mongo_client['file_hub']


fs = GridFS(mongo_database)


def save_file(data: bytes, file_name: str, content_type: str) -> str:
    file_obj_id = fs.put(
        data,
        filename=file_name,
        content_type=content_type
    )

    return str(file_obj_id)


def get_file_by_id(file_id: str) -> GridOut:
    fs.get(ObjectId(file_id))

    return fs.get(ObjectId(file_id))

