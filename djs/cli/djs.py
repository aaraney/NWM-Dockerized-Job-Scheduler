#!/usr/bin/env python3

import click

# Local imports
from djs.job_scheduler.scheduler import Scheduler
from djs.perturbation_engine.from_yaml import perturb_from_yaml


# Adapted from https://click.palletsprojects.com/en/7.x/advanced/
class AliasedGroup(click.Group):
    '''
    Allow commands to be accessed using aliases for ease on the phalanges.
    '''

    __alias_dict = {
        'js': 'job-scheduler',
        'pe': 'perturbation-engine',
    }

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        try:
            alias_cmd = self.__alias_dict[cmd_name]
        except KeyError:
            return None
        
        return click.Group.get_command(self, ctx, alias_cmd)

# djs CLI, top most click.group()
@click.group(cls=AliasedGroup)
def main():
    '''
    Is a tool for easily varying NWM/WRF-Hydro model parameters and
    running concurrent simulations inside of Docker contianers. Both the
    job-scheduler and perturbation-engine use yaml files to complete
    operations. See their help pages for more information.

    js | job-scheduler [yaml file]:\n
       Is capable of automating, managing, and executing concurrent
       NWM/Wrf-Hydro simulations for the purpose of simulating different
       model parameter scenarios. Docker image with precompiled WRF-Hydro/NWM
       binaries are used to complete simulations.

    pe | perturbation-engine [yaml file]:\n
        A tool to quickly adjust and/or stochastically vary WRF-Hydro/NWM
        model parameters to create altered parameter files. It offers the
        ability to scale parameters using mathmatical operators or randomly
        sample values and apply them to the paramter using a statistical
        distribution.
        
    '''
    pass

# Job Schdeuler CLI
@main.command('job-scheduler', short_help = 'Run concurrent NWM/WRF-Hydro simulations')
@click.argument('setup_yaml', type=click.Path(exists=True), nargs=1)
@click.option('--dry-run', '-d', required=False, is_flag=True, 
              help='Do not start jobs, instead print jobs queue')
def job_scheduler(setup_yaml, dry_run):
    '''
    Run concurrent NWM/WRF-Hydro simulations scenarios using Docker. It takes
    a directory of model related files and a list of alternative model domain
    parameter files, then the Job Scheduler maps the alternative model files
    to individual NWM/WRF-Hydro simulations. This setup information is
    contained in a yaml file as depicted below.
    
    \b
    Yaml setup file structure:
        primary: path-to-modeling-directory
        alternative-files:
            - path-to-alternative-file
            ...
            - path-to-alternative-file
        cpus: number-of-cpus to use
        max-jobs: maximum running Docker containers
        mpi-np: number of mpi jobs per container
        image: docker image to use for each container
    
    \b
    Example Yaml setup file:
        primary: 'primary'
        alternative-files:
            - 'Route_Link.nc'
            - 'Route_Link_1.nc'
            - 'Route_Link_2.nc'
            - 'Route_Link_3.nc'
            - 'Route_Link_4.nc'
        cpus: '0-7'
        max-jobs: 3
        mpi-np: 2
        image: 'aaraney/nwm-djs:2.0'

    \b
    Example primary directory structure:
        ./primary/
            namelist.hrldas
            hydro.namelist
            DOMAIN/
                Fulldom_hires.nc
                GEOGRID_LDASOUT_Spatial_Metadata.nc
                geo_em.d01.nc
                GWBUCKPARM.nc
                hydro2dtbl.nc
                LAKEPARM.nc
                nudgingParams.nc
                Route_Link.nc
                soil_properties.nc
                spatialweights.nc
                wrfinput_d01.nc
            RESTART/
                # If you are starting the model warm
                HYDRO_RST.YYYY-MM-DD_HH-MM_DOMAIN1
                RESTART.YYYYMMDDHH_DOMAIN1
            FORCING/
                # E.g., if you are using NLDAS hourly forcings
                YYYYMMDDHH.LDASIN_DOMAIN1

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
@main.command('perturbation-engine', short_help = 'Perturb NWM/WRF-Hyrdo parameter files')
@click.argument('setup_yaml', type=click.Path(exists=True), nargs=1)
def perturbation_engine(setup_yaml):
    '''
    Apply scalar or randomly sampled values to WRF-Hydro/NWM model parameters
    using in-place operator (i.e. +=, *=) operand pairs or fitted statistical
    distribution random sampling using a setup yaml file.

    \b
    Supported WRF-Hydro/NWM parameters:
        Route_link.nc: BtmWdth, ChSlp, n, nCC, TopWdth, TopWdthCC, BtmWdth
        GWBUCKPARM.nc : Expon, Zinit, Zmax
        LAKEPARM.nc : OrificeA, OrificeC, OrificeE, WeirC, WeirE, WeirL
        soil_properties.nc: mfsno
        Fulldom_hires.nc : LKSATFAC, OVROUGHRTFAC, RETDEPRTFAC

    \b
    Supported operators:
        +, -, *, /, ^ OR **, =, %, //, <<, >>

    \b
    Supported distribution:
        norm, gamma, uniform

    \b
    Yaml setup file structure:
        path-to-paramterfile.nc:
            - parameter_name:
                output <optional>: output-filename
                perturbation-method: operator operand pairs OR boolean
            - group_of_parameters:
                output <optional>: group-output-filename
                parameter_name_0:
                    perturbation-method: operator operand pairs OR boolean
                parameter_name_1:
                    perturbation-method: operator operand pairs OR boolean

    \b
    Example Yaml setup file:
        /home/example/NWM-Docker-Ensemble-Framework/pocono_test_case/Route_Link.nc:
            - group1:
                output: 'ChSlp_nCC_scalar.nc'
                ChSlp:
                    scalar: '- 2'
                nCC:
                    scalar: '* 3'
            - n:
                output: 'n_normal.nc'
                norm: True
            - TopWdthCC:
                gamma: False
                scalar: '* 1'
        /home/example/NWM-Docker-Ensemble-Framework/pocono_test_case/primary/DOMAIN/Fulldom_hires.nc:
            - LKSATFAC:
                output: ubiquitous_uniform_Fulldom_hires.nc
                uniform: True
    '''
    perturb_from_yaml(setup_yaml)


if __name__ == "__main__":
    main()