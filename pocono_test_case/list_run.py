import sys
from os.path import realpath

from scheduler import Scheduler

sys.path.append("../framework/JobScheduler")

primary_path = realpath("primary")
altered_domain_files = [
    "Route_Link.nc",
    "Route_Link_1.nc",
    "Route_Link_2.nc",
    "Route_Link_3.nc",
    "Route_Link_4.nc",
]

# Map full file system path name to altered domain files
altered_domain_files = map(lambda f: realpath(f), altered_domain_files)
schedule = Scheduler.fromList(primary_path, altered_domain_files)
schedule.max_jobs = 2
schedule.mpi_np = 2
schedule.max_cpus = "0-2"

# Begin running the containers using the job queue
# NOTE: This python script will complete while containers are
# still running. Use the command line command `docker ps` to
# check the status of running containers.
schedule.startJobs()
