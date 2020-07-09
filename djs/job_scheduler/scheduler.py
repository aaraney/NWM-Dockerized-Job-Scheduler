#!/usr/bin/env python3

import docker
import operator
import queue
from datetime import datetime
from functools import reduce
from os.path import join, dirname, realpath
from random import randint

# Local imports
from .job import Job
from .domainsetup import _setup_model


class Scheduler(object):
    '''
    djs's module responsible for scheduling and spawning jobs. A queue data
    structure is use to house jobs awaiting spawning. This Scheduler is most
    commonly referenced through its class methods.
    '''

    def __init__(self, docker_client=None):
        if docker_client:
            self.docker_client = docker_client
        else:
            # Set to system docker if one is not provided
            self._check_heart_beat()
            self.docker_client = docker.from_env()


        # unique session id for each run of scheduler
        # uses UTC time. this is appended to replica dir names
        # see classmethods for implementation
        self.schedule_id = datetime.utcnow().strftime('%y%m%d-%H%M%S')

        self.runningContainerDict = {}
        self._jobQ = queue.deque()

        self._image_tag = 'aaraney/nwm-djs:2.0'
        # Max jobs is the max number of jobs
        # running at any given time
        # TODO: Find information from system to inform this
        self._MAX_JOBS = 2

        # Max cps is the max number of cpus
        # running at any given time
        # see docker python api for help with syntax
        # https://docker-py.readthedocs.io/en/stable/containers.html
        self._MAX_CPUS = '0-1'

        # MPI np is the number of mpi processes
        # that each container will be allotted
        self._MPI_NP = 2

    @classmethod
    def from_list(cls, primary_dir, alt_domain_list):
        '''
        Fill jobs queue from list of file names.

        The alt domain list files will attempt to have their full path mapped
        to the list, however it is *best practice* to provide a list of
        absolute paths.

        alt_domain_list is accepted as nested lists, this will link the files
        in the nested list to the same simulation, thus allowing for numerous
        alternate files to be used.
        '''
        scheduler = cls()
        for i, fn in enumerate(alt_domain_list):
            # Each replica is named as such, rep-<number>-sesh-yymmdd-HMS
            replica_mnt_point = join(dirname(primary_dir), 'rep-{}-sesh-{}'.format(i, scheduler.schedule_id))

            # Handle nested alternative file list items
            fn = map(scheduler._nested_path_helper, alt_domain_list)
            job = Job(replica_mnt_point, primary_dir, fn)
            scheduler._enqueue(job)
        return scheduler

    @classmethod
    def from_yaml(cls, yaml_file):
        '''
        Fills job queue from a provided yaml file

        Note: Absolute and relative paths are accepted
        Required keys and values for yaml file(these are case sensitive)

        Alternative-files key accepts nested lists, this will link the files
        in the nested list to the same simulation, thus allowing for numerous
        alternate files to be used.

        Job Scheduler yaml format:
            primary: '/path/to/your/primary/'
            alternative-files:
                - '/path/to/alt/file'
                -
                - '/path/to/alt/file1'
                - '/path/to/alt/file2'
                ..
                - '/path/to/alt/file'

        Optional key value pairs:
            image: 'docker/image' default aaraney/nwm-djs:2.0
            max-jobs: <int> (e.g., 3) default 2
            cpus: <str> (e.g., '0-4') default '0-1'
            mpi-np: <int> (e.g., 3) default 2
        '''
        import yaml

        scheduler = cls()

        # Load the yaml file into dictionary
        with open(yaml_file) as fn:
            yml_obj = yaml.safe_load(fn)

        try:
            primary_dir = yml_obj['primary']
            alt_domain_list = yml_obj['alternative-files']

            # Get full system paths for primary domain and alt domain files
            primary_dir = realpath(primary_dir)
            alt_domain_list = map(scheduler._nested_path_helper, alt_domain_list)
        except KeyError:
            raise KeyError('Check that both `primary` and `alternative-files` are keys in yaml file.')

        # Set class property if provided in yaml
        optional_keys = {'cpus':'scheduler.max_cpus', 'image':'scheduler.image_tag',
                         'max-jobs':'scheduler.max_jobs', 'mpi-np':'scheduler.mpi_np'
                         }
        for item in optional_keys.keys():
            if item in yml_obj:
                # Set property value of schedule object using dictionary of optional keys
                exec('{} = "{}"'.format(optional_keys[item], yml_obj[item]))

        for i, file in enumerate(alt_domain_list):
            replica_mnt_point = join(dirname(primary_dir), 'rep-{}-sesh-{}'.format(i, scheduler.schedule_id))
            job = Job(replica_mnt_point, primary_dir, file)
            scheduler._enqueue(job)

        return scheduler

    def __str__(self):
        return 'mpi-np: {}\n {}'.format(self.mpi_np, str(list(map(lambda x: print('{}\n'.format(x)), list(self._jobQ)))))

    @property
    def client_list(self):
        return self.docker_client.containers.list()

    @property
    def jobQ(self):
        return self._jobQ

    @property
    def max_jobs(self):
        return self._MAX_JOBS
    @max_jobs.setter
    def max_jobs(self, max_jobs):
        self._MAX_JOBS = int(max_jobs)

    @property
    def max_cpus(self):
        return self._MAX_CPUS
    @max_cpus.setter
    def max_cpus(self, max_cpus):
        self._MAX_CPUS = max_cpus

    @property
    def mpi_np(self):
        return self._MPI_NP
    @mpi_np.setter
    def mpi_np(self, n_processes):
        self._MPI_NP = int(n_processes)

    @property
    def image_tag(self):
        return self._image_tag

    @image_tag.setter
    def image_tag(self, tag):
        self._image_tag = tag

    @image_tag.deleter
    def image_tag(self):
        self._image_tag = None

    def _nested_path_helper(self, fn):
        '''
        Helper for class methods

        If fn is a list, map realpath to items in list. Else, return realpath
        of fn.
        '''
        if type(fn) is list:
            return list(map(realpath, fn))

        else:
            return realpath(fn)

    def _check_heart_beat(self):
        '''
        Check if the Docker daemon is running
        '''
        # Currently only supporting local docker client
        # However, see https://docker-py.readthedocs.io/en/stable/client.html
        # to implement a remote docker server
        try:
            # Check for a heartbeat
            docker.from_env().ping()
        except:
            raise ConnectionError("Please check that the Docker Daemon is installed and running.")

    def check_for_image(self, image_tag):
        '''
        Check if user has specified container pulled
        '''
        docker_image_list = self.docker_client.images.list()
        # Create flattened list of RepoTags of images pulled on docker client
        docker_repo_tag_list = reduce(operator.concat, list(map(lambda x: x.attrs['RepoTags'], docker_image_list)))

        # Return bool if image is pulled
        return image_tag in docker_repo_tag_list

    def _run_job(self, job, image_tag, cpuset):
        volumes = {
            job.replica_mnt_point : {'bind': '/replica',
                     'mode': 'rw'}
        }
        try:
            job.container_id = self.docker_client.containers.run(image_tag, cpuset_cpus=cpuset, detach=True,
                                                                entrypoint='run.sh {}'.format(self.mpi_np), remove=True,
                                                                volumes=volumes)
        except docker.errors.APIError:
            job.clean()
            raise docker.errors.APIError(
                    "Removing replica directory.\n"
                    "Verify that the docker deamon can mount volumes where the primary directory is stored."
                    )

        return job

    def _enqueue(self, job):
        '''
        Add job to queue
        '''
        self._jobQ.append(job)

    def _setup_job(self, job):
        '''
        Create replica dir and link files for job
        '''
        _setup_model(job)

    def dump_all_jobs(self):
        '''
        This will NOT run any jobs in docker. Setup all jobs creating their
        replica directories and linking their alternative domain files
        properly.
        '''
        while len(self._jobQ) != 0:
            job = self._jobQ.pop()
            self._setup_job(job)
            print('''Dumped job information:
                {}'''.format(str(job).replace('\n', '\n\t')))

        self.docker_client.close()

    def start_jobs(self):
        '''
        Begin the dispersion of jobs from the job queue until the jobs queue
        has been exhausted
        '''
        # TODO: add in something for tracking jobs?

        # Check for number of running containers if greater than allotted
        if len(self.docker_client.containers.list()) > self._MAX_JOBS:
            raise Exception('System already has too many running containers. '
                            'Either kill containers or adjust the max_jobs '
                            'attribute.')
        running_containers_list = self.docker_client.containers.list()

        while len(self._jobQ) != 0:
            if len(running_containers_list) < self._MAX_JOBS:
                job = self._jobQ.pop()
                self._setup_job(job)
                running_job = self._run_job(job, self.image_tag, self._MAX_CPUS)
                print('''Simulation started:
                {}'''.format(str(running_job).replace('\n', '\n\t')))
            running_containers_list = self.docker_client.containers.list()

        # Close docker client, does not kill active containers 
        self.docker_client.close()
