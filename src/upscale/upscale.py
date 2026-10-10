import os
import numpy as np
import cv2

from concurrent.futures import ThreadPoolExecutor

from src.celery_app import celery_app
from src.mongo_client import get_file_by_id, save_file


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL_PATH = os.path.join(BASE_DIR, 'EDSR_x2.pb')


thread_pool = ThreadPoolExecutor(max_workers=4)

used_model = {}


def upscale(image_bin: bytes, model_path: str = DEFAULT_MODEL_PATH) -> bytes:
    cv2.setNumThreads(0)

    model_name = os.path.basename(model_path)
    if model_name in used_model:
        scaler = used_model[model_name]
    else:
        scaler = cv2.dnn_superres.DnnSuperResImpl_create()
        scaler.readModel(model_path)
        scaler.setModel("edsr", 2)
        used_model[model_name] = scaler

    image_bin_array = np.frombuffer(image_bin, np.uint8)
    image = cv2.imdecode(image_bin_array, cv2.IMREAD_COLOR)
    result_image_bin_array = scaler.upsample(image)

    success, result_image = cv2.imencode('.png', result_image_bin_array)

    return result_image.tobytes()

def process_upscaling(file_mongo_obj_id: str, model_path: str = DEFAULT_MODEL_PATH) -> str:
    grid = get_file_by_id(file_mongo_obj_id)

    image_bin = grid.read()

    result_image_bin = upscale(image_bin, model_path)

    result_image_bin_id = save_file(result_image_bin, grid.filename,
                                    grid.content_type)

    return str(result_image_bin_id)


@celery_app.task
def run_upscaling(file_mongo_obj_id: str, model_path: str = DEFAULT_MODEL_PATH) -> str:
    """
            :param file_mongo_obj_id: mongo_obj_image_id
            :param model_path: path to AI model
    """
    return process_upscaling(file_mongo_obj_id, model_path)
