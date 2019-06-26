%% Read netCDF file into MATLAB
% Data: Idealized run of NWM outputs

dir = '/Users/YenChia/PBenJ/nwm_runs/results/';
filetype = '.CHRTOUT_DOMAIN1';
dateformat = 'yyyymmddHH00';

% Enter first and last day of the data range in format 'yyymmddHH00' 
day_ini = 24*datenum('201801010100',dateformat);
day_fin = 24*datenum('201801020000',dateformat);

% Setup for loop to loop through model outputs in time
day = day_ini:day_fin;

% Read the first file to figure out the length of each data
file1 = strcat(dir,datestr((day(1)/24),dateformat),filetype);
N = length(ncread(file1,'streamflow'));
streamflow = zeros(N,length(day));
time = zeros(N,length(day));
feature_id = zeros(N,length(day)); %feature_id tells us the location 

for n=1:length(day)
    
    file = strcat(dir,datestr((day(n)/24),dateformat),filetype);
    streamflow(:,n) = ncread(file,'streamflow');
    time(:,n) = ncread(file,'time');
    feature_id(:,n) = ncread(file,'feature_id');
    
end
    
    
