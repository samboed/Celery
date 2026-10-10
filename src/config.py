import os


MONGO_USER = os.getenv('MONGO_USER', 'admin')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'secret-password')
MONGO_HOST = os.getenv('MONGO_HOST', 'mongo')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_DB = os.getenv('MONGO_DB', 'files')

MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"

print(MONGO_URL)

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

CELERY_BROKER_DB_IND = int(os.getenv('CELERY_BROKER_DB_IND', 0))
CELERY_BACKEND_DB_IND = int(os.getenv('CELERY_BACKEND_DB_IND', 1))

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{CELERY_BROKER_DB_IND}"
CELERY_BACKEND_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{CELERY_BACKEND_DB_IND}"
