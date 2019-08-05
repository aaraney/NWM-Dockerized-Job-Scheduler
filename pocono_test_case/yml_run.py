from os.path import realpath
import sys
sys.path.append('../framework/JobScheduler')
from scheduler import *

schedule = Scheduler.fromYaml('djs_setup.yml')
schedule.startJobs()
