import tkinter as tk
from tkinter import filedialog, messagebox
from sftp_client import SFTPClient

class SFTPClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("SFTP Client")
        self.client = None

        self.create_widgets()

    def create_widgets(self):
        # Create connection frame
        connection_frame = tk.Frame(self.master)
        connection_frame.pack(pady=10)

        tk.Label(connection_frame, text="Host:").grid(row=0, column=0)
        self.host_entry = tk.Entry(connection_frame)
        self.host_entry.grid(row=0, column=1)

        tk.Label(connection_frame, text="Port:").grid(row=1, column=0)
        self.port_entry = tk.Entry(connection_frame)
        self.port_entry.grid(row=1, column=1)

        tk.Label(connection_frame, text="Username:").grid(row=2, column=0)
        self.username_entry = tk.Entry(connection_frame)
        self.username_entry.grid(row=2, column=1)

        tk.Label(connection_frame, text="Password:").grid(row=3, column=0)
        self.password_entry = tk.Entry(connection_frame, show="*")
        self.password_entry.grid(row=3, column=1)

        self.connect_button = tk.Button(connection_frame, text="Connect", command=self.connect)
        self.connect_button.grid(row=4, column=0, columnspan=2)

        # Create file transfer frame
        transfer_frame = tk.Frame(self.master)
        transfer_frame.pack(pady=10)

        self.upload_button = tk.Button(transfer_frame, text="Upload File", command=self.upload_file)
        self.upload_button.pack(side=tk.LEFT, padx=5)

        self.download_button = tk.Button(transfer_frame, text="Download File", command=self.download_file)
        self.download_button.pack(side=tk.LEFT, padx=5)

    def connect(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            self.client = SFTPClient(host, port, username, password)
            self.client.connect()
            messagebox.showinfo("Connection", "Successfully connected to the SFTP server.")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def upload_file(self):
        if not self.client:
            messagebox.showerror("Error", "Please connect to the server first.")
            return

        file_path = filedialog.askopenfilename()
        if file_path:
            remote_path = filedialog.askstring("Remote Path", "Enter the remote path:")
            if remote_path:
                try:
                    self.client.upload_file(file_path, remote_path)
                    messagebox.showinfo("Upload", "File uploaded successfully.")
                except Exception as e:
                    messagebox.showerror("Upload Error", str(e))

    def download_file(self):
        if not self.client:
            messagebox.showerror("Error", "Please connect to the server first.")
            return

        remote_path = filedialog.askstring("Remote Path", "Enter the remote file path:")
        if remote_path:
            local_path = filedialog.asksaveasfilename()
            if local_path:
                try:
                    self.client.download_file(remote_path, local_path)
                    messagebox.showinfo("Download", "File downloaded successfully.")
                except Exception as e:
                    messagebox.showerror("Download Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SFTPClientGUI(root)
    root.mainloop()