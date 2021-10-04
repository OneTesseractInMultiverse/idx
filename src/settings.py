import os

NATS_SERVER: str = os.environ.get('NATS_SERVER')
NATS_SUBJECT: str = os.environ.get('NATS_SUBJECT')
NATS_QUEUE: str = os.environ.get('NATS_QUEUE')

MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PWD = os.environ.get('MONGO_PWD')
MONGO_DB = os.environ.get('MONGO_DB')

print(f'mongodb://{MONGO_USER}:{MONGO_PWD}@{MONGO_HOST}:27017/identity')

config: dict = {
    'NATS_SERVER': NATS_SERVER,
    'NATS_SUBJECT': NATS_SUBJECT,
    'NATS_QUEUE': NATS_QUEUE,
    'MONGO_HOST': MONGO_HOST,
    'MONGO_USER': MONGO_USER,
    'MONGO_PWD': MONGO_PWD,
    'MONGO_DB': MONGO_DB,
    'MONGO_CONNECTION_STRING': f'mongodb://{MONGO_USER}:{MONGO_PWD}@{MONGO_HOST}:27017/identity'
}

