import sys
from os.path import realpath
sys.path.append(realpath('../'))
from Validation import *
from metadataHandler import *
import pandas as pd

# --------------------------------------------------------------------------------------------------
# --------------------------- Reading in sim & obs datasets ----------------------------------------
# --------------------------------------------------------------------------------------------------
# NHD+: 4185779 = USGS 01447720 ||||||| NHD+: 44185837 USGS 01447680
# for plotting and performance metrics
beg_date = '2018-01-01 02:00:00'
end_date = '2018-06-30 00:00:00'

# Working diretory for input/output (excepet for simulated runs)
working_dir = 'C:/Users/Iman/Desktop/'
# -------------------------------- Handling observed data -----------------------------------------
USGS_id_list = ['01447720', '01447680']

# Directory to observed data
obs_data_dir_list = [working_dir + USGS_id_list[0] + '_00060.txt',
                     working_dir + USGS_id_list[1] + '_00060.txt']

# Download the USGS data
for i, USGS_id in enumerate(USGS_id_list):
    downloadusgsdata(obs_data_dir_list[i], USGS_id, '00060', '2017-12-31', '2018-07-01')

df_obs = []
df_obs_downsampled = []
df_obs_masked = []
for i, USGS_id in enumerate(USGS_id_list):
    # Read observed data
    df_obs.append(readobserved(obs_data_dir_list[i]))
    # Reformat the datetime
    df_obs[i]['Date-time'] = pd.to_datetime(df_obs[i]['Date-time'], format='%Y-%m-%d %H:%M')
    # Convert local time to UTC
    df_obs[i] = LocaltoUTC(df_obs[i])
    # Set datetime column as index
    df_obs[i].set_index('Date-time', inplace=True)
    # Downsample the observed data
    df_obs_downsampled.append(downsampler(df_obs[i]))

    df_obs_downsampled[i] = df_obs_downsampled[i].interpolate(method='linear')
    # Mask the dataset
    df_obs_masked.append(masker(df_obs_downsampled[i], beg_date, end_date))

# -------------------------------- Handling simulated data -----------------------------------------
# files_list = [
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-1-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-2-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-3-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-4-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-5-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-6-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-7-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-8-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-9-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-10-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-11-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-12-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-13-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-14-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-15-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-16-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-17-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-18-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-19-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-20-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-21-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-22-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-23-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-24-sesh-190718-192930/frxst_pts_out.txt',
# 'F:/Volumes/nwm_runs/pocono_010118-063018/frxst_out/rep-25-sesh-190718-192930/frxst_pts_out.txt'
# ]



files_list = [
'F:/Volumes/nwm_runs/pocono_extreme_case/frxst_out/rep-0-sesh-190718-224259/frxst_pts_out.txt',
'F:/Volumes/nwm_runs/pocono_extreme_case/frxst_out/rep-1-sesh-190718-224259/frxst_pts_out.txt',
'F:/Volumes/nwm_runs/pocono_extreme_case/frxst_out/rep-2-sesh-190718-224259/frxst_pts_out.txt',
]


files_list = list(map(realpath, files_list))

dict = metadataDict(files_list, 'Route_link.nc')
db_sim = frxstFilestoDFs(files_list)

df_sim_masked = []
for i, USGS_id in enumerate(USGS_id_list):
    # Reformat the datetime
    db_sim[i]['Date-time'] = pd.to_datetime(db_sim[i]['Date-time'], format='%Y-%m-%d %H:%M')
    # Set datetime column as index
    db_sim[i].set_index('Date-time', inplace=True)
    # Mask the dataset
    df_sim_masked.append(masker(db_sim[i], beg_date, end_date))

# # --------------------------------------------------------------------------------------------------
# # ---------------------- Calculate and Report the goodness of fit metrics --------------------------
# # --------------------------------------------------------------------------------------------------
# TODO: Convert to functions + handle missing data much better
for i, USGS_id in enumerate(USGS_id_list):
    for j in range(0, len(dict)):
        report_perfomance_metrics(df_sim_masked[i][dict[files_list[j]]], df_obs_masked[i]['Q_cms'],
                                  working_dir + 'perfmetr_' + str(USGS_id) + '.csv',
                                  dict[files_list[j]], runnumber=j+1)

# --------------------------------------------------------------------------------------------------
# -------------------------------------- PLOT ------------------------------------------------------
# --------------------------------------------------------------------------------------------------

color_list = ['m', 'b', 'g', 'r', 'y', 'k']

# TODO: Convert to functions
for i, USGS_id in enumerate(USGS_id_list):

    fig, (ax1) = plt.subplots(nrows = 1, ncols = 1)
    for j in range(0, len(dict)):
         ax1.plot(df_sim_masked[i][dict[files_list[j]]], linewidth=0.75, c=color_list[j], label='Sim_{}'.format(dict[files_list[j]]), marker="None", alpha=0.6)

    # Observed data
    ax1.plot(df_obs_masked[i]['Q_cms'], c='B', linestyle='dashed', linewidth=1, marker="None",label='Observed', alpha=0.9)

    # Get current axes
    ax = plt.gca()
    #  set the x and y-axis labels
    ax.set_ylabel('Discharge (cms)', fontsize=8)
    ax.set_xlabel('Date', fontsize=8)
    # # set the x and y-axis limits
    # ax.set_xlim([df_obs_masked.index[-2]-datetime.timedelta(hours=5), datetime.timedelta(minutes=10) + df_obs_masked.index[-2]])
    # ax.set_ylim([0, 10000])
    ax.grid(True)
    plt.tick_params(labelsize=6)
    # Add a title
    # plt.title('Plot!', fontsize=12)
    #  Add a legend with some customizations
    # legend = ax.legend(loc='upper right', shadow=True, fontsize=14)
    plt.legend(loc='best', fontsize=6)
    fig.set_size_inches(30, 20)
    fig.savefig(working_dir + 'Hydrograph_USGS_' + str(USGS_id) + '.png', dpi=200)
    plt.show()
