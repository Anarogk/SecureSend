import paramiko
import os
from common.encryption import encrypt_file, decrypt_file
from common.compression import compress_file, decompress_file

class SFTPClient:
    def __init__(self, host, port, username, password=None, key_filename=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, self.port, self.username, self.password, key_filename=self.key_filename)

    def disconnect(self):
        if self.client:
            self.client.close()

    def upload_file(self, local_path, remote_path, encrypt=False, compress=False):
        if encrypt:
            local_path = encrypt_file(local_path)
        if compress:
            local_path = compress_file(local_path)

        sftp = self.client.open_sftp()
        sftp.put(local_path, remote_path, callback=self._progress)
        sftp.close()

        if encrypt or compress:
            os.remove(local_path)  # Remove temporary encrypted/compressed file

    def download_file(self, remote_path, local_path, decrypt=False, decompress=False):
        sftp = self.client.open_sftp()
        sftp.get(remote_path, local_path, callback=self._progress)
        sftp.close()

        if decrypt:
            local_path = decrypt_file(local_path)
        if decompress:
            local_path = decompress_file(local_path)

    def _progress(self, transferred, total):
        print(f"Transfer progress: {transferred}/{total} bytes")

    # Implement other SFTP operations (list_files, create_directory, delete_file, etc.)