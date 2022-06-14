from minio import Minio
import os
import glob

ACCESS_KEY = os.environ.get('ACCESS_KEY', 'minio')
SECRET_KEY = os.environ.get('SECRET_KEY', 'minio123')
MINIO_CLIENT = Minio("localhost:9000", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)


def setup_bucket(bucket_name):
    try:
        found = MINIO_CLIENT.bucket_exists(bucket_name)
        if not found:
            MINIO_CLIENT.make_bucket(bucket_name)
        else:
            print("Bucket already exists")
    except Exception as err:
        print('Error while setting up bucket')
        raise err


def download_from_bucket(in_bucket_name, object):
    try:
        MINIO_CLIENT.fget_object(in_bucket_name, object, f'./{object}')
    except Exception as err:
        print('Error while downloading from bucket')
        raise err


def upload_to_bucket(local_path, out_bucket_name, minio_path):

    for local_file in glob.glob(minio_path):
        if not os.path.isfile(local_file):
            upload_to_bucket(
                local_file, out_bucket_name, f'{minio_path}/{os.path.basename(local_file)}'
            )
        else:
            remote_path = os.path.join(
                minio_path, local_file[1 + len(local_path):])
            MINIO_CLIENT.fput_object(out_bucket_name, remote_path, local_file)
