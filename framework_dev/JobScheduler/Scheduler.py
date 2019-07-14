#!/usr/bin/env python3

from os.path import join, dirname
import queue
import glob
from functools import reduce
import operator
from random import randint
import docker

# Local imports
from job import Job
from nwmdomainsetup import NwmDomainSetup

# Problem list:
# 1. There are no job mnt point collision tactics in place thus far
#    this should be implemented in fromList function. AR 7/10/19
# 2. CPU's and MAX_JOBS not well implemented at the moment


class Scheduler:

    def __init__(self, docker_client=None):
        if not docker_client:
            self.docker_client = docker.from_env()
        else:
            self.docker_client = docker_client

        self.checkHeartBeat()

        # Each run of scheduler is assigned
        # an id. This id is assigned to each
        # job of the scheduler in it's
        # directory filename
        self.schedule_id = randint(0,999)

        self.alt_domain_file_list = []

        self.runningContainerDict = {}
        self._jobQ = queue.deque()

        self._image_tag = None
        # Max jobs is the max number of jobs
        # running at any given time
        # TODO: Find information from system to inform this
        self._MAX_JOBS = 2

        # Max cps is the max number of cpus
        # running at any given time
        self._MAX_CPUS = 1

    @classmethod
    def fromList(cls, master_domain, alt_domain_list):
        '''
        Fill jobs queue from list of file names

        The alt domain list files will attempt to have
        their full path mapped to the list, however it
        is *best practice* to provide a list of absolute
        paths. Code for this in Job.py

        NOTE:
            Currently model runs are only supported that
            have a single changed domain files per run.
        '''
        scheduler = cls()
        for i,file in enumerate(alt_domain_list):
            # There are no job mnt point
            # collision tactics in place
            # thus far
            # TODO: Add file collision avoidance tactics
            mnt_point = join(dirname(master_domain), 'job-{}-session-{}'.format(i, scheduler.schedule_id))
            job = Job(mnt_point, master_domain, file)
            scheduler.enqueue(job)
        return scheduler

    def __str__(self):
        # Embarrassing implementation
        # TODO: Make the readable
        return str(list(map(lambda x: print('{}\n'.format(x)), list(self._jobQ))))

    @property
    def jobQ(self):
        return self._jobQ

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
        # TODO: Make sure that this works
        slave.container_id = self.docker_client.containers.run(image_tag, cpuset_cpus=cpuset, detach=True, remove=True, volumes=volumes)
        return slave

    def enqueue(self, job):
        '''
        Add job to queue
        '''
        self._jobQ.append(job)

    def setupJob(self, job):
        '''
        Create slave dir and link files for job
        '''
        slave = NwmDomainSetup.fromJob(job)
        return slave

    def fillJobQueue(self):
        '''
        Populate the queue with jobs to be run.
        Slave directories for each job are not created
        until they are pushed out of the queue
        '''
        pass


    def startJobs(self):
        # Check for number of running containers if greater than allotted
        if len(self.docker_client.containers.list()) >= self.MAX_JOBS:
            print("System already at set MAX_JOBS quota.")
            return None

        while len(self._jobQ) != 0:
            if len(self.docker_client.containers.list()) <= self.MAX_JOBS:
                slave = self._jobQ.pop()
                slave = self.setupJob(slave)
                # This code needs to be modernized
                self.runJob(self.image_tag, slave, '0-3')

                # Implement database for metadata here


if __name__=='__main__':
    master_domain = "/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN_DEFAULT"
    altered_domain_files = [
        "/Users/austinraney/Box Sync/si/nwm/domains/pocono/Route_Link.nc",
        "/Users/austinraney/Box Sync/si/nwm/domains/pocono/Route_Link_1.nc",
        "/Users/austinraney/Box Sync/si/nwm/domains/pocono/Route_Link_2.nc",
        "/Users/austinraney/Box Sync/si/nwm/domains/pocono/Route_Link_3.nc",
        "/Users/austinraney/Box Sync/si/nwm/domains/pocono/Route_Link_4.nc"
    ]
    schedule = Scheduler.fromList(master_domain, altered_domain_files)
    print(schedule)
    # print(list(map(lambda x: x.mnt_point, list(schedule.jobQ))))

    # slave = '/Users/austinraney/Box Sync/si/sandbox/framework_test/slave_domain'
    # print(s.runJob('aaraney/nwm-run-env', slave, '0-3'))
