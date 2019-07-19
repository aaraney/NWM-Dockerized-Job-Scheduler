import sys
from matplotlib import pyplot as plt
from os.path import realpath
sys.path.append(realpath('../'))
from Validation import frxstFilestoDFs
from metadataHandler import *

files_list = [
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-5-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-17-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-9-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-20-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-0-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-12-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-11-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-3-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-23-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-18-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-14-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-6-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-13-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-21-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-1-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-8-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-16-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-4-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-24-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-7-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-15-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-19-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-2-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-22-session-674/frxst_pts_out.txt',
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-10-session-674/frxst_pts_out.txt'
]

files_list = list(map(realpath, files_list))

df = frxstFilestoDFs(files_list, 'Route_link.nc')

df = list(map(lambda x: x.reindex(sorted(x.columns), axis=1), df))

df[0].

def plotEnsemble(df):
    '''
    This function creates a comparison plot
    to see the difference for an ensemble.

    Returns a matplotlib object
    '''
    dates = df.iloc[:, 0]
    width = len(df.columns)
    fig_size = plt.rcParams["figure.figsize"]

    for i in range(2, width):
        plt.plot(dates, df.iloc[:, i])
    plt.rcParams["figure.figsize"] = [12,9]
    plt.show()


# plotEnsemble(df[0])
