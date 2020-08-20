from pathlib import Path
import sys

import djs

schedule = djs.from_yaml('djs_setup.yml')
schedule.startJobs()
