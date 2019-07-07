#!/usr/local/bin/python3

import os
import docker
from queue import Queue

# Currently only supporting local docker client
# However, see https://docker-py.readthedocs.io/en/stable/client.html
# to implement a remote docker server
docker_client = docker.from_env()

jobQ = Queue()