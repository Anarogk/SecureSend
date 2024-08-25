from setuptools import setup, find_packages

setup(
    name="sftp_project",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "paramiko",
        "pyyaml",
        "cryptography",
        "gzip",
        "tkinter",
    ],
    entry_points={
        "console_scripts": [
            "sftp_client=sftp_project.client.gui:main",
            "sftp_server=sftp_project.server.sftp_server:main",
        ],
    },
    author="Anarogk",
    author_email="anuragmunde002@gmail.com",
    description="A secure SFTP client and server implementation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Anarogk/SecureSend",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
