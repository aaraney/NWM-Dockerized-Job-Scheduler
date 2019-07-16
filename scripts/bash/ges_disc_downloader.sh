#!/bin/bash

# A script to download a single grb and xml file from GES DISC
# This script is intended to be parrallized with xargs -P [n]
# ex: cat urls | xargs -I {} -P 16 ./ges_disc_downloader.sh {}

if [ "${1}" ];
then
	wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies -r -c -nH -nd -np -A grb,xml  --content-disposition {} 
else
	read url
	#echo $url
	wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies -r -c -nH -nd -np -A grb,xml  --content-disposition "${url}"
fi
