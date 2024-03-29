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


def delete_gif(filename, bucket_name):
    try:
        MINIO_CLIENT.remove_object(bucket_name, filename)
    except Exception as e:
        print('Error while deleting a gif')
        raise e


def delete_all_elements(bucket_name):
    try:
        obj_list = MINIO_CLIENT.list_objects(bucket_name)
        for obj in obj_list:
            MINIO_CLIENT.remove_object(bucket_name, obj.object_name)
    except Exception as err:
        print('Error while deleting all elements in the bucket')
        raise err


def delete_bucket(bucket_name):
    try:
        delete_all_elements(bucket_name)
        MINIO_CLIENT.remove_bucket(bucket_name)
    except Exception as err:
        print('Error while deleting the bucket')
        raise err


def list_all_files(bucket_name):
    try:
        obj_list = MINIO_CLIENT.list_objects(bucket_name)
        return obj_list
    except Exception as err:
        print('Error while listing files in the bucket')
        raise err   


def get_elements(bucket_name):
    try:
        all_gifs = list_all_files(bucket_name)
        binary_gifs = []
        for gif in all_gifs:
            elt = MINIO_CLIENT.get_object(bucket_name, gif.object_name)
            binary_gifs.append({
                'name': gif.object_name,
                'data': elt,
            })
        return binary_gifs
    except Exception as e:
        print("Failed while getting elements")
        return [] 

