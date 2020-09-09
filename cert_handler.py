# cert_handler.py

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class CertHandler(object):

    def __init__(self, parameter_list):
        pass

    @staticmethod
    def generate_key(keyname: str, passphrase: str, filelocation:str="./pki/"):
        """
        Generate a Public/Private key file to be used by the certificate
        """

        # generate public/private key file.
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        # write key to file
        with open("./pki/key.pem", "wb") as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase")
            ))


    def _generate_certificate_signing_request(self, username, key):
        """
        Generate the certificate signing request for the new user in Kubernetes
        """

        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes

        # generate a certificate signing request to be signed by kubernetes
        csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u"{0}".format(username))
        ])
        ).sign(key, hashes.SHA256(), default_backend())

        # write CSR to file
        with open("./pki/csr.pem", "wb") as f:
            f.write(csr.public_bytes(serialization.Encoding.PEM))

    



        
    
