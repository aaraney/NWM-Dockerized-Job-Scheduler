import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import glob, os
# import xarray as xr
import pandas as pd
from datetime import datetime, timedelta
import math
# import HydroErr as he  # Library for goodness of fit functions, Note: it still misses some (e.g., PB, RSR...)
# from pytz import timezone
# import pytz


# --------------------------------------------------------------------------------------------------
# ---------------------------- Goodness of fit functions -------------------------------------------
# --------------------------------------------------------------------------------------------------

def NSE(SimulatedStreamFlow, ObservedStreamFlow):
    '''(SimulatedStreamFlow, ObservedStreamFlow)'''
    x = SimulatedStreamFlow
    y = ObservedStreamFlow
    A = 0.0  # dominator
    B = 0.0  # deminator
    tot = 0.0
    for i in range(0, len(y)):
        tot = tot + y[i]
    average = tot / len(y)
    for i in range(0, len(y)):
        A = A + math.pow((y[i] - x[i]), 2)
        B = B + math.pow((y[i] - average), 2)
    E = 1 - (A / B)  # Nash-Sutcliffe model eficiency coefficient
    return E

# Define definition for Percent Bias model efficiency coefficient---used up in the class
def PB(SimulatedStreamFlow, ObservedStreamFlow):
    '''(SimulatedStreamFlow, ObservedStreamFlow)'''
    x = SimulatedStreamFlow
    y = ObservedStreamFlow
    A = 0.0  # dominator
    B = 0.0  # deminator
    for i in range(0, len(y)):
        A = A + (y[i] - x[i])
        B = B + y[i]
    PB = (A / B)  # Percent Bias model eficiency coefficient
    return PB

def R2(SimulatedStreamFlow, ObservedStreamFlow):
    R = np.corrcoef(SimulatedStreamFlow, ObservedStreamFlow)[0, 1]
    R2 = math.pow(R, 2)  # Corelation coefficient
    return R2  # 0 is the best and + 1 is the worst

def RSR(SimulatedStreamFlow, ObservedStreamFlow):
    '''(SimulatedStreamFlow, ObservedStreamFlow)'''

    x = SimulatedStreamFlow
    y = ObservedStreamFlow
    A = 0.0  # dominator
    B = 0.0  # deminator
    tot = 0.0
    for i in range(0, len(y)):
        tot = tot + x[i]
    average = tot / len(x)
    for i in range(0, len(y)):
        A = A + math.pow((y[i] - x[i]), 2)
        B = B + math.pow((y[i] - average), 2)
    RSR = (math.pow(A/B, 0.5))  # RMSE-observations standard deviation ratio (RSR) https://www.mdpi.com/2306-5338/1/1/20/htm
    return RSR


# --------------------------------------------------------------------------------------------------
# ----------------------- Reading in sim & obs datasets functions-----------------------------------
# --------------------------------------------------------------------------------------------------

# TODO: handle observed data better. Maybe somehow use the WRES USGS reader function in R!!, otherwise download the data
# here and then tweak the following function a little bit..
def readobserved(directory):
    '''(Observed data directory)'''
    # Creating data frame for observed discharge
    df = pd.read_csv(directory, header=0, sep=',', parse_dates=True,  # index_col=0
                         infer_datetime_format=True)
    return df


def readNWMoutput_netcdf(directory, feature_id):
    '''(NWM output directory, feature_id as integer)'''
    # This function, reads the discharge from NWM netcdf ouput files
    os.chdir(directory)

    mfdataDIR = directory + '*.CHRTOUT_DOMAIN1'
    DS = xr.open_mfdataset(mfdataDIR)
    time = (DS.time.values).ravel()
    dQ = (DS.sel(feature_id= feature_id).streamflow.values).ravel()
    # plt.plot(dQ,'r-')
    # plt.show()

    # Creating data frame for simulated discharge
    columns = ['tz_cd', 'Discharge']
    df_sim = pd.DataFrame(index=time, columns=columns)

    df_sim['Discharge'] = dQ
    df_sim['tz_cd'] = 'UTC'

    return df_sim


def readNWMoutput_csv(directory):
    '''(Simulated data directory)'''
    # This function creates data frame for one NWM simulation time series
    colnames = ['Seconds', 'datetime', 'ReachID', 'Lon', 'Lat', 'discharge_cms', 'discharge_cfs',
                'FlowDepthOrRiverStage']
    df = pd.read_csv(directory, header=None, names=colnames,
                         sep=',', parse_dates=True, index_col=None, infer_datetime_format=True)
    df.drop(['Seconds', 'ReachID', 'Lon', 'Lat', 'discharge_cms', 'FlowDepthOrRiverStage'], axis=1, inplace=True)
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')

    return df

def readNWMoutput_csv_ensemble(frxst_files):
    '''
    Input: List of frxst points files from NWM
    Output: List of Datafile objects

    Each item in the returned list is a dataframe object where each
    dataframe relates to a unique NHDplus node from the frxst points files.

    In each dataframe the cols relate to a specific
    frxst points file.
    '''
    if not type(frxst_files) is list:
        raise TypeError

    dateframe_col_names = ['Date-time', 'NHDplus_link', 'Q_cms']
    joined_df = pd.read_csv(frxst_files[0], header=None, names=dateframe_col_names, sep=',', parse_dates=True
                         ,index_col=None, usecols=[1, 2, 6])

    # Set to capture unique NHDplus_links
    unique_stations = set(joined_df['NHDplus_link'])

    # If only one file in frxst_files, pass
    try:
        for file in frxst_files[1:]:
            # join dataframe with columns date, NHDPlus link, and Q in cms
            df = pd.read_csv(file, header=None, names=['Q_cms'], sep=',',
                             parse_dates=False, index_col=None, usecols=[6])
            joined_df = pd.concat([joined_df, df], axis=1)
    except:
        pass

    return [joined_df[joined_df.NHDplus_link == x] for x in unique_stations]

# The following function, currently, only handles gages in Central time Zone. To be more generalized. It is also not that fast.
def LocaltoUTC(df):
    '''(Dataframe)'''
    # Convert local time to UTC (Note: Python libraries for handing time zone does not work properly for USGS data)
    start_time = datetime.now()
    for i in range(len(df)):  # takes 70 seconds for 2 years with 15-minute sampling interval

        if df['tz_cd'][i] == 'CST':
            df.loc[[i], 'datetime'] = df.datetime[i] + timedelta(hours=6)

        elif df_obs['tz_cd'][i] == 'CDT':
            df.loc[[i], 'datetime'] = df.datetime[i] + timedelta(hours=5)

    df = df.sort_values(by='datetime', ascending=True)  # Sorts the data based on timestamp. Check the lines 28128 - 28136 before sorting to see the problem!
    df_obs['tz_cd'] = 'UTC'
    print('Took this amount of time to convert local-time to UTC: ', datetime.now() - start_time)
    return df

def upsampler(df):
    '''(Dataframe)'''
    # Up-sample to 15 minute (from 1 hour) to be comparable to USGS Obs (necessary for calculating the evaluation metrics)
    df_upsampled = df.resample('15T')
    df_interpolated = df_upsampled.interpolate(method='linear')

    return df_interpolated


def downsampler(df):
    '''(Dataframe)'''
    # Down-sample to 1 hour (from 15 min)
    df_downsampled = df.resample('1H').mean()

    return df_downsampled

def masker(df, beg_date, end_date):
    '''(Dataframe,beg_date, end_date )'''
    mask = (df.index >= beg_date) & (df.index <= end_date)
    df_masked = df.loc[mask]

    return df_masked

# TODO: to be more generalized to handle any metrics that given to function as a list (not just the 4 current ones)...
def report_perfomance_metrics(SimulatedStreamFlow, ObservedStreamFlow, reportfile_directory, runnumber = 1):
    '''(SimulatedStreamFlowDataFrame, ObservedStreamFlowDataFrame, reportfile_directory)'''
    # Before using this function, the simulated and observed datframes must be processed to have dishcarge values
    # in same time span and at the same temporal resolution and same exact times.

    if len(SimulatedStreamFlow) != len(ObservedStreamFlow):
        raise ValueError("Length of simulated and observed datframes are not the same!")


    NSE = he.nse(SimulatedStreamFlow, ObservedStreamFlow)
    PercentBias = 100 * PB(SimulatedStreamFlow, ObservedStreamFlow)
    RMSE = he.rmse(SimulatedStreamFlow, ObservedStreamFlow)
    R_squared = he.r_squared(SimulatedStreamFlow, ObservedStreamFlow)

    if runnumber == 1:
        printline = ''
        printline += printline + 'RunNumber,NSE,PB,RMSE,R_squared\n'
        f = open(os.path.join(reportfile_directory, "PerfMetrReport.csv"), "w")
        f.writelines(printline)
        f.close()

    printline = ''
    printline += '\n'
    printline = 'Run ' + str(runnumber) + ' ,'
    printline += '{0:.3f},{1:.3f},{2:.3f},{3:.3f}' \
        .format(NSE, PercentBias, RMSE, R_squared)

    printline += '\n'
    f = open(os.path.join(reportfile_directory, "PerfMetrReport.csv"), "a")
    f.writelines(printline)
    f.close()

    return NSE, PercentBias, RMSE, R_squared


# --------------------------------------------------------------------------------------------------
# --------------------------- Reading in sim & obs datasets ----------------------------------------
# --------------------------------------------------------------------------------------------------
# beg_date = '2011-03-05 01:00:00'
# end_date = '2011-03-19 00:00:00'
# Runnumbers = [1, 2, 3, 4]
#
# # Directory to observed data
# obs_data_dir = 'C:/Users/Iman/Desktop/02450250_1.csv'
#
# # Directory to simulated data
# # sim_data_dir = 'C:/Users/Iman/Desktop/chan_05_2011_frxst_pts_out.txt' # for one simulated time series. Not for ensemble
# sim_data_dir = r'C:\Users\Iman\Desktop'
#
#
# # Read observed data
# df_obs = readobserved(obs_data_dir)
# # Reformat the datetime
# df_obs['datetime'] = pd.to_datetime(df_obs['datetime'], format='%m/%d/%Y %H:%M')
# # Convert local time to UTC
# df_obs = LocaltoUTC(df_obs)
# # Set datetime column as index
# df_obs.set_index('datetime', inplace=True)
# df_obs['tz_cd'] = 'UTC'
# # Donwsample the observed data
# df_obs_downsampled = downsampler(df_obs)
# # Mask the dataset
# df_obs_masked = masker(df_obs_downsampled, beg_date, end_date)
#
#
# # # Read simulated data
# # df_sim = readNWMoutput_csv(sim_data_dir)
# # # Set datetime column as index
# # df_sim.set_index('datetime', inplace=True)
# # # Mask the dataset
# # df_sim_masked = masker(df_sim, beg_date, end_date)
#
#
# # Read ensemble of simulated discharge
# df_sim = readNWMoutput_csv_ensemble(sim_data_dir)
# # Mask the dataset
# df_sim_masked = masker(df_sim, beg_date, end_date)
#
#
# # # --------------------------------------------------------------------------------------------------
# # # ---------------------- Calculate and Report the goodness of fit metrics --------------------------
# # # --------------------------------------------------------------------------------------------------
# # TODO: check R_squared, also I assumed that we have only 4 runs
# for Runnumber in Runnumbers:
#     report_perfomance_metrics(df_sim_masked['discharge_cfs_Run_{}'.format(Runnumber)], df_obs_masked['Discharge'],
#                               'C:/Users/Iman/Desktop/', runnumber=Runnumber)
#
# # --------------------------------------------------------------------------------------------------
# # -------------------------------------- PLOT ------------------------------------------------------
# # --------------------------------------------------------------------------------------------------
# # TODO: if needed the plot part will be converted to function to better visualize Ensemble output
#
# fig, (ax1) = plt.subplots(nrows = 1, ncols = 1)
# # IMPORTANT! Fake data!
# for Runnumber in Runnumbers:
#     ax1.plot(df_sim_masked['discharge_cfs_Run_{}'.format(Runnumber)]*(Runnumber/4.0), linewidth=0.5, marker="None", label='Sim_{}'.format(Runnumber), alpha=0.6)
#
# # Important: Fake mean
# ax1.plot(df_sim_masked['discharge_cfs_Run_1']*1.2/2.0, c='g', linestyle='dashdot', linewidth=1.5, marker="None", label='Sim_Mean', alpha=0.9)
# # Observed data
# ax1.plot(df_obs_masked['Discharge'], c='B', linestyle='dashed', linewidth=1.5, marker="None",label='Observed', alpha=0.9)
#
# # Get current axes
# ax = plt.gca()
# #  set the x and y-axis labels
# ax.set_ylabel('Discharge (cfs)', fontsize=8)
# ax.set_xlabel('Date', fontsize=8)
# # # set the x and y-axis limits
# # ax.set_xlim([df_obs_masked.index[-2]-datetime.timedelta(hours=5), datetime.timedelta(minutes=10) + df_obs_masked.index[-2]])
# # ax.set_ylim([0, 10000])
# ax.grid(True)
# plt.tick_params(labelsize=6)
# # Add a title
# # plt.title('Plot!', fontsize=12)
# #  Add a legend with some customizations
# # legend = ax.legend(loc='upper right', shadow=True, fontsize=14)
# plt.legend(loc='best', fontsize=6)
# fig.set_size_inches(30, 20)
# fig.savefig('C:/Users/Iman/Desktop/Hydrograph.png', dpi=200)
# plt.show()
#

