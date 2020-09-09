# cert_handler.py

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from pathlib import Path

filelocation: str = "./pki/"


def _ensure_cert_working_path():
    Path(Path.cwd().joinpath(filelocation)).mkdir(parents=True, exist_ok=True)
    return Path(Path.cwd().joinpath(filelocation))


class CertHandler(object):

    def __init__(self, parameter_list):
        pass

    @staticmethod
    def generate_key(keyname: str, passphrase: str):
        """
        Generate a Public/Private key file to be used by the certificate
        """

        file_location = _ensure_cert_working_path()

        key_file = Path(file_location).joinpath(f"{keyname}_key.pem")

        # generate public/private key file.
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        # write key to file
        with open(key_file, "wb") as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(bytes(passphrase, "utf-8"))
            ))

        if key_file.is_file():
            return key_file
        else:
            return None

    @staticmethod
    def generate_certificate_signing_request(username, passphrase, key_file):
        """
        Generate the certificate signing request for the new user in Kubernetes
        """

        file_location = _ensure_cert_working_path()

        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes

        key_bytes = None
        with open(key_file, "rb") as f:
            key_bytes = f.read()

        key = serialization.load_pem_private_key(key_bytes, bytes(passphrase, "utf-8"), default_backend())

        csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        # Provide various details about who we are.
            x509.NameAttribute(NameOID.COMMON_NAME, u"{0}".format(username)),
        ])).sign(key, hashes.SHA256(), default_backend())

        csr_file = Path(file_location).joinpath(f"{username}_csr.pem")

        # write CSR to file
        with open(csr_file, "wb") as f:
            f.write(csr.public_bytes(serialization.Encoding.PEM))

        if csr_file.is_file():
            return csr_file
        else:
            return None
