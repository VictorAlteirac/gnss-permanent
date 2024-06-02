# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:29:08 2024

@author: victor
"""

from utils import *
import gnsscal
from datetime import date

year=2024
month=5
day=18

#Definition des variables par défaut
gnss_day=gnsscal.date2doy(date(year, month, day))
gnss_week=gnsscal.date2gpswd(date(year, month, day))

py_path=os.getcwd()

station_list_sira=['sete', 'mtp2', 'mntp', 'yscn', 'gajn', 'sgil']
station_list_stein=['pzna', 'agds', 'agde', 'sete', 'narb', 'pard', 'mtp2']
site='SIRA'
path_download=py_path+"\DOWNLOAD\Donwload_file_RGP"

file_path=path_download+'/'+site+'/'+str(year)+'/'+str(gnss_day)+'/obs'
file_path_nav=path_download+'/'+site+'/'+str(year)+'/'+str(gnss_day)+'/nav'
       
download_rinex_obs(year, gnss_day, station_list_sira, site, path_download)
uncrompress_Z_file(file_path)
uncompact_rinex_file_hatanaka(file_path)
delete_useless_file(file_path)

uncrompress_Z_file_nav(file_path_nav)
Donwload_SIRA_day(year, month, day, station_list_sira, site, path_download, gnss_day)
unzip_SIRA_file(year, gnss_day)
