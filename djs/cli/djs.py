#!/usr/bin/env python3

# CLI library import
import click

# Local imports
# Job Scheduler related imports
from djs.job_scheduler.scheduler import Scheduler

# Perturbation engine related imports
from djs.perturbation_engine import parameter_editor

# djs CLI, top most click.group()
@click.group()
def main():
    '''
    The Dockerized Job Scheduler (djs) is capable of automating, managing,
    and executing numerous NWM simulations simultaneously. This framework was
    designed with the intent of removing the overhead of model setup and
    compilation, thereby lowering the barrier for entry without limiting
    performance. In doing so, facilitating an environment for scientists to
    more easily test hypotheses.
    '''
    pass

# Job Schdeuler CLI
@main.group()
def job_scheduler():
    from djs.job_scheduler.scheduler import Scheduler

@job_scheduler.command()
@click.argument('setup_yaml', nargs=1)
@click.option('--dry-run', '-d', required=False, is_flag=True, 
              help='Do not start jobs, instead print jobs queue')
def from_yaml(setup_yaml, dry_run):
    '''
    Start Wrf-Hydro/NWM simulations from provided yaml setup file
    '''

    scheduler = Scheduler.fromYaml(setup_yaml)

    # If the --dry-run flag is passed, 
    # print jobs in the queue don't start jobs
    if dry_run:
        for job in scheduler.jobQ:
            click.echo(job)

    else:
        scheduler.startJobs()

# Perturbation engine CLI
@main.command()
def perturbation_engine():
    pass

if __name__ == "__main__":
    main()