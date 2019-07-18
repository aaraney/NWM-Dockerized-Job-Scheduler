import sys
from matplotlib import pyplot as plt
from os.path import realpath
sys.path.append(realpath('../'))
from Validation import frxstFilestoDFs

files_list = [
<<<<<<< HEAD:framework/perturb_py_dev/val_test.py
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
'/Users/austinraney/Box Sync/si/nwm/runs/pocono/replica-10-session-674/frxst_pts_out.txt',
]

files_list = list(map(lambda x: realpath, files_list))

df = readNWMoutput_csv_ensemble(files_list)

dfa = df[0]
plt.plot(dfa.iloc[:,0], dfa.iloc[:,1])
plt.show()

def plotEnsemble(df):
    '''
    This function creates a comparison plot
    to see the difference for an ensemble.

    Returns a matplotlib object
    '''
    dates = df.iloc[:,0]
    width = len(df.columns)

    for i in range(1, width):
        plt.plot(dates, df.iloc[:, i])

    plt.show()
