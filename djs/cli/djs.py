#!/usr/bin/env python3

# CLI library import
import click

# Local imports
# Job Scheduler related imports
from djs.job_scheduler.scheduler import Scheduler

# Perturbation engine related imports
from djs.perturbation_engine.parameter_editor import edit_parameters

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
@click.option('--input', '-i', required=False,
            help='Input WRF-Hydro/NWM static domain file')
@click.option('--parameter', '-p', required=False,
            help='WRF-Hydro/NWM parameter for varying within the input file')
@click.option('--scalar', '-s', required=False, nargs=2, #type=click.Tuple([str, float]),
help='''Use a provided scalar to adjust the provided WRF-Hydro/NWM parameter (i.e. + 2)
\nAvailable operators include:
\n\t=, +, -, *, /, ^ or **, %, //, <<, >>''')
@click.option('--output', '-o', required=False,
    help='Output file netcdf file for storing perturbed parameter file')
def perturbation_engine(**kwargs):
    
    # Check that kwarg values are not None. Checking empty list condition 
    # not [] -> True
    if [v for v in kwargs.values() if v is not None]:
        print('here')
        _input = kwargs['input']
        parameter = [kwargs['parameter']]
        op_args = [kwargs['scalar'][0]]
        value_args = list(map(float, list(kwargs['scalar'][1])))

        print(f'{_input}\n{parameter}\n{op_args}\n{value_args}')
        # output = kwargs['output']

        df = edit_parameters(_input, parameter, op_args, value_args)
        print(df)

    else:
        pass


if __name__ == "__main__":
    main()