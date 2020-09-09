#!/usr/bin/python3

# ktl to copy kubernetes config

from client import RemoteClient
from cert_handler import CertHandler
import getpass
import argparse


def main(hostname, username, ssh_key_file, passwd):

    # create certs for username
    key_file = CertHandler.generate_key(username, passwd)
    csr_file = CertHandler.generate_certificate_signing_request(username, passwd, key_file)

    # transfer csr to server


    # sign csr to create certificate








    remote = RemoteClient(hostname, username, passwd, ssh_key_file)

    # do these commands
    remote.execute_commands(['pwd', 'ls', 'whoami'])

    commands = [
        ''
    ]


    remote.disconnect()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("server", type=str, help="server address to connect to")
    parser.add_argument("-u", "--user", help="set ssh user - defaults to current user")
    parser.add_argument("-i", "--identity", help="set the SSH identity (key) to be used - defaults to ~/.ssh/id_rsa")

    args = parser.parse_args()

    user = args.user if args.user is not None else getpass.getuser()  # getpass.getuser()
    host = args.server
    key_file = args.identity if args.identity is not None else r'~/.ssh/id_rsa'
    password = getpass.getpass(f'Enter password for keyfile \'{key_file}\' : ')
    main(host, user, key_file, password)
