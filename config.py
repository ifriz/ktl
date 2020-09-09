# config

from os import environ

host = environ.get('REMOTE_HOST')
user = environ.get('REMOTE_USER')
ssh_key_path = environ.get('SSH_KEY')

remote_path = environ.get('REMOTE_PATH')
local_path = '/data'