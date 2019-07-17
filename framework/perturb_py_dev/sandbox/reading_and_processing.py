import sys
from os.path import realpath
sys.path.append(realpath('../'))
from Validation import *

# --------------------------------------------------------------------------------------------------
# --------------------------- Reading in sim & obs datasets ----------------------------------------
# --------------------------------------------------------------------------------------------------
beg_date = '2018-01-01 02:00:00'
end_date = '2018-06-31 00:00:00'
Runnumbers = [1, 2, 3, 4]

# Directory to observed data
obs_data_dir = 'C:/Users/Iman/Desktop/02450250_1.csv'

# Directory to simulated data
# sim_data_dir = 'C:/Users/Iman/Desktop/chan_05_2011_frxst_pts_out.txt' # for one simulated time series. Not for ensemble
sim_data_dir = r'C:\Users\Iman\Desktop'


# Read observed data
df_obs = readobserved(obs_data_dir)
# Reformat the datetime
df_obs['datetime'] = pd.to_datetime(df_obs['datetime'], format='%m/%d/%Y %H:%M')
# Convert local time to UTC
df_obs = LocaltoUTC(df_obs)
# Set datetime column as index
df_obs.set_index('datetime', inplace=True)
df_obs['tz_cd'] = 'UTC'
# Donwsample the observed data
df_obs_downsampled = downsampler(df_obs)
# Mask the dataset
df_obs_masked = masker(df_obs_downsampled, beg_date, end_date)


# Read simulated data
df_sim = readNWMoutput_csv(sim_data_dir)
# Set datetime column as index
df_obs.set_index('datetime', inplace=True)
df_obs['tz_cd'] = 'UTC'
# Donwsample the observed data
df_obs_downsampled = downsampler(df_obs)
# Mask the dataset
df_obs_masked = masker(df_obs_downsampled, beg_date, end_date)


# # Read simulated data
# df_sim = readNWMoutput_csv(sim_data_dir)
# # Set datetime column as index
# df_sim.set_index('datetime', inplace=True)
# # Mask the dataset
# df_sim_masked = masker(df_sim, beg_date, end_date)


# Read ensemble of simulated discharge
df_sim = readNWMoutput_csv_ensemble(sim_data_dir)
# Mask the dataset
df_sim_masked = masker(df_sim, beg_date, end_date)


# # --------------------------------------------------------------------------------------------------
# # ---------------------- Calculate and Report the goodness of fit metrics --------------------------
# # --------------------------------------------------------------------------------------------------
# TODO: check R_squared, also I assumed that we have only 4 runs
for Runnumber in Runnumbers:
    report_perfomance_metrics(df_sim_masked['discharge_cfs_Run_{}'.format(Runnumber)], df_obs_masked['Discharge'],
                              'C:/Users/Iman/Desktop/', runnumber=Runnumber)

# --------------------------------------------------------------------------------------------------
# -------------------------------------- PLOT ------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# TODO: if needed the plot part will be converted to function to better visualize Ensemble output

fig, (ax1) = plt.subplots(nrows = 1, ncols = 1)
# IMPORTANT! Fake data!
for Runnumber in Runnumbers:
    ax1.plot(df_sim_masked['discharge_cfs_Run_{}'.format(Runnumber)]*(Runnumber/4.0), linewidth=0.5, marker="None", label='Sim_{}'.format(Runnumber), alpha=0.6)

# Important: Fake mean
ax1.plot(df_sim_masked['discharge_cfs_Run_1']*1.2/2.0, c='g', linestyle='dashdot', linewidth=1.5, marker="None", label='Sim_Mean', alpha=0.9)
# Observed data
ax1.plot(df_obs_masked['Discharge'], c='B', linestyle='dashed', linewidth=1.5, marker="None",label='Observed', alpha=0.9)

# Get current axes
ax = plt.gca()
#  set the x and y-axis labels
ax.set_ylabel('Discharge (cfs)', fontsize=8)
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
fig.savefig('C:/Users/Iman/Desktop/Hydrograph.png', dpi=200)
plt.show()
