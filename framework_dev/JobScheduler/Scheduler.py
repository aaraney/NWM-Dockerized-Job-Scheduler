#!/usr/local/bin/python3

import os
import docker
from JobScheduler.Job import Job
from queue import Queue

# Currently only supporting local docker client
# However, see https://docker-py.readthedocs.io/en/stable/client.html
# to implement a remote docker server
# docker_client = docker.from_env()

jobQ = Queue()

if __name__=='__main__':
    j = Job('test','test','test','test')
    print(j)
