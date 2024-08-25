import os
import paramiko


class FileManager(paramiko.SFTPServerInterface):
    def __init__(self, root="/tmp/sftp"):
        self.root = root

    def _realpath(self, path):
        return os.path.join(self.root, path.lstrip("/")) # converting path to absolute path

    def list_folder(self, path):
        path = self._realpath(path) #listing contents
        try:
            # returning SFTPAttributes for each item in the directory
            return [paramiko.SFTPAttributes.from_stat(os.stat(os.path.join(path, f))) for f in os.listdir(path)]
        except OSError:
            return []

    def stat(self, path):
        path = self._realpath(path)
        try:
            return paramiko.SFTPAttributes.from_stat(os.stat(path))
        except OSError:
            return paramiko.SFTPAttributes()

    def lstat(self, path):
        path = self._realpath(path)
        try:
            # Returning SFTPAttributes using lstat
            return paramiko.SFTPAttributes.from_stat(os.lstat(path))
        except OSError:
            return paramiko.SFTPAttributes()

    def open(self, path, flags, attr):
        path = self._realpath(path)
        try:
             # Ensure the file is opened in binary mode if necessary
            binary_flag = getattr(os, 'O_BINARY', 0)
            flags |= binary_flag
            mode = getattr(attr, 'st_mode', None)
            if mode is not None:
                fd = os.open(path, flags, mode)
            else:
                fd = os.open(path, flags)
            # Returning handle to opened file
            return paramiko.SFTPHandle(fd)
        except OSError:
            return None

    def remove(self, path):
        path = self._realpath(path)
        try:
            os.remove(path)
        except OSError:
            return paramiko.SFTP_FAILURE
        return paramiko.SFTP_OK

    def rename(self, oldpath, newpath):
        oldpath = self._realpath(oldpath)
        newpath = self._realpath(newpath)
        try:
            os.rename(oldpath, newpath)
        except OSError:
            return paramiko.SFTP_FAILURE
        return paramiko.SFTP_OK

    def mkdir(self, path, attr):
        path = self._realpath(path)
        try:
            os.mkdir(path)
        except OSError:
            return paramiko.SFTP_FAILURE
        return paramiko.SFTP_OK

    def rmdir(self, path):
        path = self._realpath(path)
        try:
            os.rmdir(path)
        except OSError:
            return paramiko.SFTP_FAILURE
        return paramiko.SFTP_OK
