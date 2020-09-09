# RemoteClient

""" Remote host object to handle connections and actions """

import sys
from loguru import logger
from os import system
from paramiko import SSHClient, AutoAddPolicy, MissingHostKeyPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException

logger.add(sys.stderr,
           format="{time} {message}",
           filter="client",
           level="INFO")

logger.add('logs/log_{time:YYYY-MM-DD}.log',
           format="{time} {level} {message}",
           filter="client",
           level="ERROR")


class RemoteClient(object):
    """Client to interact with remote host via ssh and scp"""

    def __init__(self, host, user, password, ssh_key_filepath):
        super(RemoteClient, self).__init__()
        self.host = host
        self.user = user
        self.password = password
        self.ssh_key_filepath = ssh_key_filepath
        self.ssh_key = None
        # self.remote_path = remote_path
        self.client = None
        self.scp = None
        # self.__get_ssh_key()

    # self.__upload_ssh_key()

    def __get_ssh_key(self):
        """ Fetch local ssh key """
        try:
            self.ssh_key = RSAKey.from_private_key_file(self.ssh_key_filepath, self.password)
            logger.info(f'Found SSH key at {self.ssh_key_filepath}')
        except SSHException as error:
            logger.error(error)

        return self.ssh_key

    # def __upload_ssh_key(self):
    # 	try:
    # 		system(f'ssh')
    # 	except Exception as e:
    # 		raise e

    def __connect(self):

        try:
            logger.info('Attempting Authentication')
            self.client = SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(MissingHostKeyPolicy())
            self.client.connect(self.host,
                                username=self.user,
                                password=self.password,
                                key_filename=self.ssh_key_filepath,
                                look_for_keys=True,
                                timeout=5000)
            logger.info('Successfully Authenticated')
            # self.scp = SCPClient(self.client.get_transport())
        except AuthenticationException as e:
            logger.error('Authentication failed.')
            logger.error(e)
            raise e
        except Exception as err:
            logger.error('connection failed')
            logger.error(err)
            raise err
        finally:
            return self.client

    def disconnect(self):
        """Close the ssh connection"""
        self.client.close()
        # self.scp.close()

    def execute_commands(self, commands):
        """execute multiple commands in succession"""
        if self.client is None:
            try:
                self.client = self.__connect()
            except Exception as err:
                logger.error("server connection failed")
                self.client.close()
                return

        for cmd in commands:
            logger.info(f'Executing: {cmd}')
            stdin, stdout, stderr = self.client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            for line in response:
                logger.info(f'INPUT: {cmd} | OUTPUT: {line}')

