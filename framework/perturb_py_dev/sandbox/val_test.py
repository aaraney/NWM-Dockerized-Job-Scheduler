import sys
from os.path import realpath
sys.path.append(realpath('../'))
from Validation import frxstFilestoDFs

files_list = [
'/Volumes/si_ar/pocono_25/pocono_2/replica-2-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-10-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-6-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-17-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-3-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-24-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-7-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-15-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-1-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-21-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-4-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-13-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-18-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-19-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-12-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-11-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-14-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-23-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-20-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-8-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-5-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-0-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-22-session-674/frxst_pts_out.txt',
'/Volumes/si_ar/pocono_25/pocono_2/replica-9-session-674/frxst_pts_out.txt',
]

db =frxstFilestoDFs(files_list)
