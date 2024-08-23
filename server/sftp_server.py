import paramiko
import socket
import threading
from server.auth import authenticate_user
from server.file_manager import FileManager

class SFTPServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        return authenticate_user(username, password)

    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_exec_request(self, channel, command):
        self.event.set()
        return True

def start_server(host, port, key_file):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)

    while True:
        client, addr = sock.accept()
        print(f"Connection from: {addr}")
        t = threading.Thread(target=handle_client, args=(client, key_file))
        t.start()

def handle_client(client, key_file):
    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(paramiko.RSAKey(filename=key_file))
        server = SFTPServer()
        transport.start_server(server=server)
        channel = transport.accept(20)
        if channel is None:
            print("No channel.")
            return

        sftp_server = paramiko.SFTPServer(channel, FileManager())
        sftp_server.serve_forever()
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        try:
            transport.close()
        except:
            pass

if __name__ == "__main__":
    start_server("0.0.0.0", 2222, "server_key.pem")