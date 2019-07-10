#!/usr/local/bin/python3

import os
import docker
from JobScheduler.Job import Job
from queue import Queue
import glob
from functools import reduce
import operator


class Scheduler:

    def __init__(self, docker_client=None):
        if not docker_client:
            self.docker_client = docker.from_env()
        else:
            self.docker_client = docker_client

        self.checkHeartBeat()

        self.alt_domain_file_list = []

        self.runningContainerDict = {}
        self.jobQ = Queue()

        self._image_tag = None
        # Max jobs is the max number of jobs
        # running at any given time
        self._MAX_JOBS = 1

        # Max cps is the max number of cpus
        # running at any given time
        self._MAX_CPUS = 1

    @property
    def MAX_JOBS(self):
        return self._MAX_JOBS
    @MAX_JOBS.setter
    def MAX_JOBS(self, max_jobs):
        self._MAX_JOBS = max_jobs

    @property
    def MAX_CPUS(self):
        return self._MAX_CPUS
    @MAX_CPUS.setter
    def MAX_CPUS(self, max_cpus):
        self._MAX_CPUS = max_cpus

    @property
    def image_tag(self):
        return self._image_tag

    @image_tag.setter
    def image_tag(self, tag):
        self._image_tag = tag

    @image_tag.deleter
    def image_tag(self):
        self._image_tag = None


    def checkHeartBeat(self):
        # Currently only supporting local docker client
        # However, see https://docker-py.readthedocs.io/en/stable/client.html
        # to implement a remote docker server
        try:
            docker_client = docker.from_env()
            # Check for a heartbeat
            docker_client.ping()
        except ConnectionError:
            print("Please check that the Docker Daemon is running.")
            exit(1)

    def check_for_image(self, image_tag):
        # Check if user has specified container pulled
        docker_image_list = self.docker_client.images.list()
        # Create flattened list of RepoTags of images pulled on docker client
        docker_repo_tag_list = reduce(operator.concat, list(map(lambda x: x.attrs['RepoTags'], docker_image_list)))

        # Return bool if image is pulled
        return image_tag in docker_repo_tag_list

    def runJob(self, image_tag, slave, cpuset):
        volumes = {
            slave : {'bind': '/slave',
                     'mode': 'rw'}
        }
        return self.docker_client.containers.run(image_tag, cpuset_cpus=cpuset, detach=True, remove=True, volumes=volumes)

    def startJobs(self):
        while self.jobQ.qsize() != 0:
            container_list = self.docker_client.containers.list()
            if len(container_list) < self.MAX_JOBS:
                self.runJob()



            self.docker_client.containers.run(self.image_tag, entrypoint='something')
            client.containers.run('alpine', 'echo hello world')

        job = Job()




if __name__=='__main__':
    s = Scheduler()
    slave = '/Users/austinraney/Box Sync/si/sandbox/framework_test/slave_domain'
    print(s.runJob('aaraney/nwm-run-env', slave, '0-3'))

