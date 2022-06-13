from minio import Minio
from minio.error import InvalidResponseError
from dotenv import load_dotenv
import os
import glob
load_dotenv()
LOCAL_FILE_PATH = os.environ.get('LOCAL_FILE_PATH')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
MINIO_API_HOST = "http://localhost:9000"
MINIO_CLIENT = Minio("localhost:9000", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)


def setting_up_bucket(bucket_name):
    try:
        MINIO_CLIENT.make_bucket(bucket_name)
    except InvalidResponseError as err:
        raise


def downloading_from_bucket(in_bucket_name, object):
    try:
        MINIO_CLIENT.fget_object(in_bucket_name, object, f'./{object}')
    except InvalidResponseError as err:
        raise


def uploading_to_bucket(local_path, out_bucket_name, minio_path):

    for local_file in glob.glob(minio_path):
        if not os.path.isfile(local_file):
            uploading_to_bucket(
                local_file, out_bucket_name, f'{minio_path}/{os.path.basename(local_file)}'
            )
        else:
            remote_path = os.path.join(
                minio_path, local_file[1 + len(local_path):])
            MINIO_CLIENT.fput_object(out_bucket_name, remote_path, local_file)
