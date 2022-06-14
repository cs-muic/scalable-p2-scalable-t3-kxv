from minio import Minio
import os
import glob

ACCESS_KEY = os.environ.get('ACCESS_KEY', 'minio')
SECRET_KEY = os.environ.get('SECRET_KEY', 'minio123')
MINIO_CLIENT = Minio("minio-service:9000", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)


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


def download_bucket(in_bucket_name):
    try:
        for item in MINIO_CLIENT.list_objects(in_bucket_name,recursive=True):
                    MINIO_CLIENT.fget_object(in_bucket_name,item.object_name, f'./{in_bucket_name}/{item.object_name}')
    except Exception as err:
        print('Error while downloading a bucket')
        raise err


def upload_to_bucket(local_dir, out_bucket_name):
    try:
        cwd = os.getcwd()
        local_path = f'{cwd}/{local_dir}'
        for local_file in glob.glob(local_path + '/**'):
            remote_path = local_file[1 + len(local_path):]
            MINIO_CLIENT.fput_object(out_bucket_name, remote_path, local_file)
    except Exception as err:
        print('Error while uploading to the bucket')
        raise err

def upload_gif(filename, out_bucket_name):
    try:
        cwd = os.getcwd()
        local_file = f'{cwd}/{filename}'
        MINIO_CLIENT.fput_object(out_bucket_name, filename, local_file)
    except Exception as err:
        print('Error while uploading to the bucket')
        raise err

def delete_bucket(bucket_name):
    try:
        MINIO_CLIENT.remove_bucket(bucket_name)
    except Exception as err:
        print('Error while deleting the bucket')
        raise err
