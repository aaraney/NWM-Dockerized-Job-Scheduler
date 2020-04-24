import sys

from scheduler import Scheduler

# from os.path import realpath


sys.path.append("../framework/JobScheduler")

schedule = Scheduler.fromYaml("djs_setup.yml")
schedule.startJobs()
