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
import gzip

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
            rename_o=crx_file.replace('crx', 'o')
            rename_rnx=crx_file.replace('crx', 'rnx')
            os.rename(rename_rnx, rename_o)

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
        
    if day>10: 
        day=str(day)
    else:
        day='0'+str(day)
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
    
    donwload_path = os.getcwd()+'/DOWNLOAD/Donwload_file_RGP/SIRA'+"/"+str(year)+'/'+str(gnss_day)+'/'+'IGS'
    
    try:
        os.mkdir(donwload_path)
    except: 
        pass
    
    filename_sp3='IGS0OPSRAP_'+str(year)+str(gnss_day)+'0000_01D_15M_ORB.SP3.gz'
    filename_clk='IGS0OPSRAP_'+str(year)+str(gnss_day)+'0000_01D_05M_CLK.CLK.gz'
    
    donwload_sp3_path=donwload_path+'/'+filename_sp3
    ftp.retrbinary("RETR " + filename_sp3, open(donwload_sp3_path,'wb').write)
    
    donwload_clk_path=donwload_path+'/'+filename_clk
    ftp.retrbinary("RETR " + filename_clk, open(donwload_clk_path,'wb').write)
    
    
    with gzip.open(donwload_clk_path, 'rb') as fclk:
      file_content_1 = fclk.read()

    donwload_clk_path_un=donwload_clk_path.replace('.CLK.gz', 'SP3')
    with open(donwload_clk_path_un+'.clk', "wb") as binary_file_1:
      # Write bytes to file
      binary_file_1.write(file_content_1)
      
      '''-----'''
      
    with gzip.open(donwload_sp3_path, 'rb') as f:
      file_content = f.read()
    
    donwload_sp3_path_un=donwload_sp3_path.replace('.SP3.gz', 'SP3')
    with open(donwload_sp3_path_un+'.sp3', "wb") as binary_file:
      # Write bytes to file
      binary_file.write(file_content)
      
    os.remove(donwload_clk_path)
    os.remove(donwload_sp3_path)

    
#%%Calul GNSS
def calcul_GNSS_RTK_LIB(site, site_num ,year, month, day, gnss_day, gnss_week, rgp_obs_file):
    root_path=os.getcwd()
    folder_process=str(year)+str(month)+str(day)
    process_path=root_path+'/PROCESS_RESULT/'+folder_process
    try: 
        os.mkdir(process_path)
    except: 
        pass
    
    py_path=os.getcwd()
    RTK_LIB=py_path+'\\RTKLIB\\bin\\rnx2rtkp.exe '
    config_file=py_path+'\\RTKLIB\\config_file.conf '
    
    obs_nav_file_folder=py_path+'\\DOWNLOAD\\Donwload_file_RGP\\'+site+'\\'+str(year)+'\\'+str(gnss_day)+'\\Antenne\\'
    list_obs=os.listdir(obs_nav_file_folder)
    for item in list_obs: 
        if 'o' in item: 
            obs_file=obs_nav_file_folder+item+' '
        if 'p' in item: 
            nav_file=obs_nav_file_folder+item+' '
    
    rgp_obs=py_path+'\\DOWNLOAD\\Donwload_file_RGP\\'+site+'\\'+str(year)+'\\'+str(gnss_day)+'\\obs\\'+rgp_obs_file+str(gnss_day)+'0.o '
    
    sp3_file=py_path+'\\DOWNLOAD\\Donwload_file_RGP\\'+site+'\\'+str(year)+'\\'+str(gnss_day)+'\\IGS\\'+'IGS0OPSRAP_'+str(year)+str(gnss_day)+'0000_01D_15M_ORBSP3.sp3 '
    clk_file=py_path+'\\DOWNLOAD\\Donwload_file_RGP\\'+site+'\\'+str(year)+'\\'+str(gnss_day)+'\\IGS\\'+'IGS0OPSRAP_'+str(year)+str(gnss_day)+'0000_01D_05M_CLKSP3.clk '
    
    out_file=process_path+'\\'+rgp_obs_file+'_result.out'
    
    command=RTK_LIB+obs_file+rgp_obs+nav_file+sp3_file+clk_file+'-k '+config_file+' -o '+out_file
        
    os.system(command)
    
    return out_file
    
