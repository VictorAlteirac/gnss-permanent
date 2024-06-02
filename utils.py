# -*- coding: utf-8 -*-+
"""
Created on Mon May 27 11:27:01 2024

@author: victor
"""
import ftplib 
import unlzw3
from pathlib import Path
import os 
from tqdm import tqdm
import zipfile

def download_rinex_obs(year, gnss_day, station_list, site, path_download):
    
    path = 'pub/data/'+str(year)+'/'+str(gnss_day)+'/data_30'
    ftp = ftplib.FTP("rgpdata.ign.fr") 
    ftp.login() 
    ftp.cwd(path)
    donwload_path = path_download+'/'+site
    try: 
        os.mkdir(donwload_path+'/'+str(year))
    except: 
        pass
    try: 
        os.mkdir(donwload_path+'/'+str(year)+'/'+str(gnss_day))
    except: 
        pass
    
    donwload_full_path=donwload_path+'/'+str(year)+'/'+str(gnss_day)
    try: 
        os.mkdir(donwload_full_path+'/obs')
    except: 
        pass
    try: 
        os.mkdir(donwload_full_path+'/nav')
    except: 
        pass
        
    for station in tqdm(range(len(station_list))):
        #Observation dtata
        filename = station_list[station]+str(gnss_day)+'0.24d.Z'
        donwload_station_path=donwload_full_path+'/obs/'+filename
        ftp.retrbinary("RETR " + filename, open(donwload_station_path,'wb').write)
        
        #GPS nav data
        filename = station_list[station]+str(gnss_day)+'0.24n.Z'
        donwload_nav_path=donwload_full_path+'/nav/'+filename
        ftp.retrbinary("RETR " + filename, open(donwload_nav_path,'wb').write)
        
        #Glonass Nav data
        filename = station_list[station]+str(gnss_day)+'0.24g.Z'
        donwload_nav_path=donwload_full_path+'/nav/'+filename
        ftp.retrbinary("RETR " + filename, open(donwload_nav_path,'wb').write)
        
    ftp.quit()


def uncrompress_Z_file(file_path): 
    list_file=os.listdir(file_path)
    for file in list_file:
        new_file=file.replace('24d.Z', 'crx')
        uncompressed_data = unlzw3.unlzw(Path(file_path+'/'+file))
        with open(file_path+'/'+new_file, 'wb') as f:
            f.write(uncompressed_data)
            f.close()

def uncrompress_Z_file_nav(file_path_nav): 
    list_file=os.listdir(file_path_nav)
    for file in list_file:
        if '24n.Z' in file: 
            new_file=file.replace('24n.Z', 'n')
        if '24g.Z' in file: 
            new_file=file.replace('24g.Z', 'g')
        print(file)
        uncompressed_data = unlzw3.unlzw(Path(file_path_nav+'/'+file))
        with open(file_path_nav+'/'+new_file, 'wb') as f:
            f.write(uncompressed_data)
            f.close()
            
        os.remove(file_path_nav+'/'+file)

def uncompact_rinex_file_hatanaka(file_path): 
    list_file=os.listdir(file_path)
    py_path=os.getcwd()
    hatanaka_path=py_path+'/RNXCMP_4.1.0_Windows_mingw_64bit/bin/CRX2RNX.exe'
    for file in list_file:
        if 'crx' in file: 
            crx_file=file_path+'/'+file
            os.system(hatanaka_path+' '+crx_file)

def delete_useless_file(file_path): 
    list_file=os.listdir(file_path)
    for file in list_file:
        if '.Z' in file or '.crx' in file: 
            file_delete=file_path+'/'+file
            os.remove(file_delete)
            
def Donwload_SIRA_day(year, month, day, station_list, site, path_download, gnss_day):
    
    if month>10: 
        month=str(month)
    else:
        month='0'+str(month)
    path = '/FTP/SIRA/0712/'+str(year)+'/'+month+'/'+str(day)
    ftp = ftplib.FTP("192.9.200.231") 
    ftp.login('GPS', ']!HlKi') 
    ftp.cwd(path)
    
    donwload_path = os.getcwd()+'/DOWNLOAD/Donwload_file_RGP/SIRA'+"/"+str(year)+'/'+str(gnss_day)+'/'+'Antenne'
    try: 
        os.mkdir(donwload_path)
    except: 
        pass
    
    filename = '0712'+str(gnss_day)+'0.24o.zip'
        
    donwload_station_path=donwload_path+'/'+filename
    ftp.retrbinary("RETR " + filename, open(donwload_station_path,'wb').write)
    ftp.quit()
    ftp.close()
           
def unzip_SIRA_file(year, gnss_day): 
    donwload_path = os.getcwd()+'/DOWNLOAD/Donwload_file_RGP/SIRA'+"/"+str(year)+'/'+str(gnss_day)+'/'+'Antenne'
    # os.listdir(donwload_path)
    file_path=donwload_path+'/'+os.listdir(donwload_path)[0]
    with zipfile.ZipFile(file_path, "r", zipfile.ZIP_DEFLATED) as zip:
        zip.extractall(donwload_path) 
    os.remove(file_path)

def Donwload_IGS_product(gnss_week, gnss_day, year):
    
    path = 'pub/products/ephemerides/'+str(gnss_week[0])
    ftp = ftplib.FTP("rgpdata.ign.fr") 
    ftp.login() 
    ftp.cwd(path)
    # donwload_path = path_download+'/'+site
    
    filename_sp3='IGS0OPSRAP_'+str(year)+str(gnss_day)+'0000_01D_15M_ORB.SP3.gz'
    filename_clk='IGS0OPSRAP_'+str(year)+str(gnss_day)+'0000_01D_05M_CLK.CLK.gz'
    
    ftp.retrbinary("RETR " + filename, open(donwload_station_path,'wb').write)

#%%Calul GNSS
