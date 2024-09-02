import gzip
import shutil

def compress_file(file_path):
    with open(file_path, 'rb') as file_in:
        with gzip.open(file_path + '.gz', 'wb') as file_out:
            shutil.copyfileobj(file_in, file_out)
    return file_path + '.gz'

def decompress_file(file_path):
    with gzip.open(file_path, 'rb') as file_in:
        with open(file_path[:-3], 'wb') as file_out:
            shutil.copyfileobj(file_in, file_out)
    return file_path[:-3]
