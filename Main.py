# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:29:08 2024

@author: victor
"""

from utils import *
import gnsscal
from datetime import date
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import dates
import tkinter as tk




#Definition des variables par défaut
def dobnwload_gnss(year, month, day): 
    gnss_day=gnsscal.date2doy(date(year, month, day))
    gnss_week=gnsscal.date2gpswd(date(year, month, day))
    
    print(gnss_day)
    
    py_path=os.getcwd()
    
    station_list_sira=['mtp2', 'mntp', 'yscn', 'gajn', 'sgil']
    station_list_stein=['pzna', 'agds', 'agde', 'narb', 'pard', 'mtp2']
    site='SIRA'
    
    if site == 'SIRA': 
        site_num=str('0712')
    if site == 'STEIN': 
        site_num=str('0830')
        
    path_download=py_path+"\DOWNLOAD\Donwload_file_RGP"
    
    #Récuparation des données d'observation et de navigation
    file_path=path_download+'/'+site+'/'+str(year)+'/'+str(gnss_day)+'/obs'
    file_path_nav=path_download+'/'+site+'/'+str(year)+'/'+str(gnss_day)+'/nav'
    text_box.delete('1.0', tk.END)
    
    try: 
        print('Telechargement des fichiers RINEX d\'observation...')
        download_rinex_obs(year, gnss_day, station_list_sira, site, path_download)
        uncrompress_Z_file(file_path)
        uncompact_rinex_file_hatanaka(file_path)
        delete_useless_file(file_path)
    
        print('Telechargement des fichiers RINEX de navigation...')
        uncrompress_Z_file_nav(file_path_nav)
    except: 
        text_box.insert("end", "fichier Rinex RGP manquant ou deja telechargé \n") # adds text to text bo
    
    
    print('Telechargement des fichiers RINEX de l\'antenne...')
    try: 
        Donwload_SIRA_day(year, month, day, station_list_sira, site, path_download, gnss_day)
        unzip_SIRA_file(year, gnss_day)
    except: 
        text_box.insert("end", "fichier Rinex SIRA manquant ou deja telechargé \n") # adds text to text bo
    
    try: 
        print('Telechargement des éphémérides precise et correction horloge...')
        Donwload_IGS_product(gnss_week, gnss_day, year)
    except: 
        text_box.insert("end", "Ephémérides ou clock manquant ou indisponible \n")
        
    text_box.insert("end", "Données télécharger avec succees \n")  
        
    print('Telechargement terminée')
    

def process_gnss(year, month, day):
    
    py_path=os.getcwd()
    
    text_box.delete('1.0', tk.END)
    
    station_list_sira=['mtp2', 'mntp', 'yscn', 'gajn', 'sgil']
    station_list_stein=['pzna', 'agds', 'agde', 'narb', 'pard', 'mtp2']
    site='SIRA'
    site_num='0712'
    
    gnss_day=gnsscal.date2doy(date(year, month, day))
    gnss_week=gnsscal.date2gpswd(date(year, month, day))
    
    print("CALCUL DES COORDONNEES SUR PLUSIEURS STATIONS...")
    coordinates_stat=[]
    observation_time=[]
    base_line=[]
    for rgp in tqdm(station_list_sira):
        
        try: 
            out_file=calcul_GNSS_RTK_LIB(site, site_num ,year, month, day, gnss_day, gnss_week, rgp)
            file = open(out_file, "r")
            result = file.readlines()
            ref_coordinates=result[23]
            
            time=int(result[7][28:30])
            observation_time.append(time)
            
            result=result[-1]
            array=np.array([float(result[26:38]), float(result[41:52]), float(result[56:68])])
            coordinates_stat.append(array)
            
            array_ref=np.array([float(ref_coordinates[15:26]), float(ref_coordinates[29:40]), float(ref_coordinates[42:54])])
            
            baseline=math.sqrt(abs(array[0]**2-array_ref[0]**2)+abs(array[1]**2-array_ref[1]**2)+abs(array[2]**2-array_ref[2]**2))
            print(baseline)
            base_line.append(baseline)
        except: 
            text_box.insert("end", "Eurreur sur l'antenne RGP :") # adds text to text bo
            text_box.insert("end", rgp) 
         
    
    observation_time=np.array(observation_time)
    base_line=np.array(base_line)
    
    poids=np.min(base_line)/base_line
    
    
    final=np.c_[coordinates_stat, base_line, observation_time, poids]
    mean=np.mean(final, axis=0)
    
    text_box.insert("end", "Données journalières calculées avec succees \n")  
    
    print('Données journalière calculé')


    #%%Calcul de la moyenne pondéré
    x_mean=final[:,[0]].reshape(5)
    y_mean=final[:,[1]].reshape(5)
    z_mean=final[:,[2]].reshape(5)
    
    x_poids=x_mean*poids
    y_poids=y_mean*poids
    z_poids=z_mean*poids
    
    x_final=np.sum(x_poids)/np.sum(poids)
    y_final=np.sum(y_poids)/np.sum(poids)
    z_final=np.sum(z_poids)/np.sum(poids)

#%%SAVE RESULT
    path_download=py_path+"\\PROCESS_RESULT\\TOTAL_RESULT.txt"
    
    with open(path_download, "a") as myfile:
        myfile.write(str(gnss_day)+'\t'+str(x_final) +'\t' +str(y_final)+'\t'+ str(z_final))
        myfile.write('\n')
    
#%%plot result
def plot_ecart():
    
    py_path=os.getcwd()
    path_download=py_path+"\\PROCESS_RESULT\\TOTAL_RESULT.txt"
    
    lines = np.loadtxt(path_download, comments="#", delimiter="\t", unpack=False)
    base_coordinates=np.array([4614730.1723, 315963.4502, 4376880.0330]).T
    
    lines=lines[lines[:, 0].argsort()]
    
    date=lines[:,0]
    xpoints = lines[:, 1]
    ypoints = lines[:, 2]
    zpoints = lines[:, 3]
    
    ecart_x=xpoints-base_coordinates[0]
    ecart_y=ypoints-base_coordinates[1]
    ecart_z=zpoints-base_coordinates[2]
    
    fig, ax = plt.subplots()
    ax.plot(date, ecart_x, color='b', label='x')
    ax.plot(date, ecart_y, color='r', label='y')
    ax.plot(date, ecart_z, color='g', label='z')
    
    # ax.xaxis.set_major_formatter(dates.DateFormatter('%y%m%d'))
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%f'))
    ax.legend(['x', 'y', 'z'])
    plt.xlabel("GNSS_Day")
    plt.ylabel("Ecarts")
    
    plt.show()



mainwindow=tk.Tk()
mainwindow.title("Calculator")
mainwindow.geometry('800x200')

year_leb = tk.Label(mainwindow, text="Calcul de GNSS : ", bg="lightgrey")
year_leb.grid(row=0, column=1)

#Ligne 1
year_leb = tk.Label(mainwindow, text="Année : ", bg="lightgrey")
year_leb.grid(row=0, column=2)

month_lab = tk.Label(mainwindow, text="Mois : ", bg="lightgrey")
month_lab.grid(row=0, column=3)

day_lab = tk.Label(mainwindow, text="Jour : ", bg="lightgrey")
day_lab.grid(row=0, column=4)

#Ligne 2
enter_info = tk.Label(mainwindow, text="Entrer la date de calcul : ", bg="lightgrey")
enter_info.grid(row=1, column=1)

year_info = tk.Entry(mainwindow, bd=3)
year_info.grid(row=1, column=2, padx=5, pady=5)

mont_info = tk.Entry(mainwindow, bd=3)
mont_info.grid(row=1, column=3, padx=5, pady=5)

day_info = tk.Entry(mainwindow, bd=3)
day_info.grid(row=1, column=4, padx=5, pady=5)

def getentry_download():
    year_var = int(year_info.get())
    month_var =int(mont_info.get())
    day_var = int(day_info.get())
    
    dobnwload_gnss(year_var, month_var, day_var)
    
def process_gnss_tk():
    year_var = int(year_info.get())
    month_var =int(mont_info.get())
    day_var = int(day_info.get())
    
    process_gnss(year_var, month_var, day_var)
    
def stat_global(): 
    py_path=os.getcwd()
    path_download=py_path+"\\PROCESS_RESULT\\TOTAL_RESULT.txt"
    
    lines = np.loadtxt(path_download, comments="#", delimiter="\t", unpack=False)
    
    xyz=lines[:,[1,2,3]]
    mean=np.mean(xyz, axis=0)
    std=np.std(xyz, axis=0)
    
    print(mean)
    print(std)
    
    text_box.delete('1.0', tk.END)
    
    text_box.insert("end", mean) # adds text to text bo
    text_box.insert("end", "\n")
    text_box.insert("end", std)
    
    return mean, std

def get_dernier_jour(): 
    py_path=os.getcwd()
    path_download=py_path+"\\PROCESS_RESULT\\TOTAL_RESULT.txt"
    
    lines = np.loadtxt(path_download, comments="#", delimiter="\t", unpack=False)
    
    day=lines[:,0]
    max_day=int(np.max(day))
    
    day_year=gnsscal.yrdoy2date(2024, max_day)
    
    text_box.delete('1.0', tk.END)
    text_box.insert("end", day_year) # adds text to text bo
    

get_day = tk.Button(mainwindow, text ="Get Last Day", command = get_dernier_jour)
get_day.grid(row=1, column=5, padx=5, pady=5)
    

#Button

T_button = tk.Button(mainwindow, text ="Telechargement Data", command = getentry_download)
T_button.grid(row=2, column=2, padx=5, pady=5)

C_button = tk.Button(mainwindow, text ="Process GNSS day", command = process_gnss_tk)
C_button.grid(row=2, column=3, padx=5, pady=5)

Plot_button = tk.Button(mainwindow, text ="Plot result", command = plot_ecart)
Plot_button.grid(row=2, column=4, padx=5, pady=5)

Plot_button = tk.Button(mainwindow, text ="Get Stat", command = stat_global)
Plot_button.grid(row=3, column=3, padx=5, pady=5)

text_box = tk.Text(mainwindow, width = 70, height = 3)
text_box.grid(row = 4, column = 2, columnspan=3)


tk.mainloop()

    
