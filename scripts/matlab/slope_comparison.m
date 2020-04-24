%% Read netCDF file into MATLAB
% Data: Idealized run of NWM outputs

dir_default = '/Users/YenChia/PBenJ/idealized_slope_comparison/default_slope_idealized/';
dir_50 = '/Users/YenChia/PBenJ/idealized_slope_comparison/slope_50_idealized/';
filetype = '.CHRTOUT_DOMAIN1';
dateformat = 'yyyymmddHH00';

% Enter first and last day of the data range in format 'yyymmddHH00' 
day_ini = 24*datenum('202001010100',dateformat);
day_fin = 24*datenum('202001020000',dateformat);

% Setup for loop to loop through model outputs in time
day = day_ini:day_fin;

% Read the first file to figure out the length of each data
file1 = strcat(dir_default,datestr((day(1)/24),dateformat),filetype);
N = length(ncread(file1,'streamflow'));
ncdisp(file1);
id = ncread(file1,'feature_id');
streamflow_default = zeros(N,length(day));
streamflow_50 = zeros(N,length(day));

% feature_id of the outlet (from frxst_pts_out.txt)
id_out = 18578829;
index_out = find(id==id_out);

for n=1:length(day)
    
    file_default = strcat(dir_default,datestr((day(n)/24),dateformat),filetype);
    streamflow_default(:,n) = ncread(file_default,'streamflow');
    
    file_50 = strcat(dir_50,datestr((day(n)/24),dateformat),filetype);
    streamflow_50(:,n) = ncread(file_50,'streamflow');
    
    
end
    
%% plots

fontsize = 18;

%figure of streamflow vs time of all sites (default side slope)
figure(1)
plot(streamflow_default')
title('Channel side slope 0.05 (default)','Interpreter','latex','FontSize',fontsize)
ylabel('m$^3$/s','Interpreter','latex','FontSize',fontsize)
xlabel('hr','Interpreter','latex','FontSize',fontsize)
xlim([1 24])
saveas(gcf,'/Users/YenChia/PBenJ/figures/Default_slope.png')

%figure of streamflow vs time of all sites (slope 50)
figure(2)
plot(streamflow_50')
title('Channel side slope 0.55','Interpreter','latex','FontSize',fontsize)
ylabel('m$^3$/s','Interpreter','latex','FontSize',fontsize)
xlabel('hr','Interpreter','latex','FontSize',fontsize)
xlim([1 24])
saveas(gcf,'/Users/YenChia/PBenJ/figures/Slope_50.png')

%figure of streamflow vs time of outlets (default and slope_50)
figure(3)
plot(streamflow_default(index_out,:)); hold on
plot(streamflow_50(index_out,:));
title('Streamflow at Outlet','Interpreter','latex','FontSize',fontsize)
legend('Default side slope: 0.05','Side slope: 0.55',...
    'Interpreter','latex','FontSize',14)
ylabel('m$^3$/s','Interpreter','latex','FontSize',fontsize)
xlabel('hr','Interpreter','latex','FontSize',fontsize)
xlim([1 24])
saveas(gcf,'/Users/YenChia/PBenJ/figures/outlet_comparison.png')
