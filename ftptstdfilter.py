import ftplib
from ftplib import FTP
import csv
import numpy as np
import gdal
from PIL import Image
import osr
import time
import os
from os import path

Ftp_Server_host = '103.16.223.166'
Ftp_username ='splzppi'
Ftp_password = 'splzppi2012'
ftp = FTP(Ftp_Server_host)
ftp.login(user=Ftp_username, passwd=Ftp_password)
print("connected to remote server :" + Ftp_Server_host)

#n cycle 145-64 (+1)
#sample n = 10 (2016-11-21 : 2017-03-27), n 1 2016, 11 ,21
#Konversi dari tanggal ke siklus,
# titik awal
# 62 kalo n 1 in:2016-11-21
# 63 kalo n 2 in:2016-11-21 + 14
# 64 kalo n 3 in:2016-11-21 + 14*2

# titik akhir
# n=2 kalo in:2016-11-21 + 14
# n=3 kalo in:2016-11-21 + 14*2

import datetime
import pandas as pd
# OutNam = raw_input(" Input tanggal : ")
basey = 2016
basem = 11
based = 21
#Input tanggal awal
inputy = 2016
inputm = 11
inputd = 22
#Input tanggal akhir
inputye = 2017
inputme = 3
inputde = 27
basedate = datetime.date(basey, basem, based)
inputdate = datetime.date(inputy, inputm, inputd)
inputdatee = datetime.date(inputye, inputme, inputde)
print(inputdate)
print(inputdatee)

tsbase = pd.Timestamp(year = basey,  month = basem, day = based) 
tsinput = pd.Timestamp(year = inputy,  month = inputm, day = inputd)
p = 2457651.5
cc = int (tsbase.to_julian_date() - p) #konversi ke C
delta = (inputdate - basedate).days
if int(delta)%14  == 0:
  cc = cc + delta/14
else:
  for i in range(14):
    inputdateup = inputdate+datetime.timedelta(i) #ditarik ke siklus depan terdekat
    delta = (inputdateup - basedate).days
    if int(delta)%14  == 0:
      cc = cc + delta/14
    else : inputdateup = inputdate

deltae = (inputdatee - basedate).days
if int(deltae)%14  == 0:
  cc2 = deltae/14 +1
else:
  for i in range(14):
    inputdateupe = inputdatee-datetime.timedelta(i) #ditarik ke siklus belakang terdekat
    deltae = (inputdateupe - basedate).days
    if int(deltae)%14  == 0:
      cc2 = deltae/14 +1
    else : inputdateupe = inputdatee
print(cc2)
print(cc)
n = cc2

siklus = []
for i in range(n):
    if i+62 < 100:
        siklus.append('C0' + str(i+cc))
    else :
        siklus.append('C' + str(i+cc))

x = datetime.date(2016, 11, 21) #Date siklus pertama 2016, 11, 21 (RSP30)
y = []
m = []
d = []

for i in range(n):
    dt = datetime.timedelta(14*(i+cc-62))
    y.append((x + dt).year)
    m.append((x + dt).month)
    d.append((x + dt).day)

datename = []
for i in range(n):
    if m[i]<10:
        m[i] = "0" + str(m[i])
    if d[i]<10:
        d[i] = "0" + str(d[i])

    datename.append(str(y[i]) + str(m[i]) + str(d[i]))
base = '/data_buffer/buffer_SAR/ALOS2_PALSAR2/JJ-FAST/'
kotak = 'S06E107'
RSP = 'RSP030'

Ftp_source_files_path = []
filenamel = []
filenamehh = []
filenamehv = []

unlist = []
ufilel = []
ufilehh = []
ufilehv = []


for i in range(n):
  Ftp_source_files_path.append( base + siklus[i] + '_' + datename[i] + '/' + kotak + '/')
  filenamel.append(kotak + '_' + datename[i] + '_' + siklus[i] + '_' + RSP + '_linci.tif')
  filenamehh.append(kotak + '_' + datename[i] + '_' + siklus[i] + '_' + RSP + '_sl_HH.tif')
  filenamehv.append(kotak + '_' + datename[i] + '_' + siklus[i] + '_' + RSP + '_sl_HV.tif')
  try:
    ftp.cwd(Ftp_source_files_path[i])
    print(Ftp_source_files_path[i] + " Connected and downloading...")
    try:
      ftp.retrbinary("RETR " + filenamel[i], open(filenamel[i], 'wb').write)
      print (Ftp_source_files_path[i] + filenamel[i] + " Completed!")
    except:
      ufilel.append(filenamel[i])
    try:
      ftp.retrbinary("RETR " + filenamehh[i], open(filenamehh[i], 'wb').write)
      print (Ftp_source_files_path[i] + filenamehh[i] + " Completed!")
    except:
      ufilehh.append(filenamehh[i])
    try:
      ftp.retrbinary("RETR " + filenamehv[i], open(filenamehv[i], 'wb').write)
      print (Ftp_source_files_path[i] + filenamehv[i] + " Completed!")
    except:      
      ufilehv.append(filenamehv[i])
  except:
    unlist.append(Ftp_source_files_path[i])

for i in range(len(unlist)):
    Ftp_source_files_path.remove(unlist[i])

with open("outputlist.csv", "wb") as f:
    writer = csv.writer(f)
    for l in Ftp_source_files_path:
        writer.writerow([l])

for i in range(len(ufilel)):
  os.remove(ufilel[i])
  filenamel.remove(ufilel[i])
  filenamehh.remove(ufilehh[i])

for i in range(len(ufilehv)):
  os.remove(ufilehv[i])
  filenamehv.remove(ufilehv[i])
for i in range(len(ufilehh)):
  os.remove(ufilehh[i])
  
n=len(filenamel)
filenamelo = []
filenamehvo = []
filenamehho = []
for i in range(n):
    if path.exists(filenamel[i]) == True:
        filenamelo.append (filenamel[i])
    if path.exists(filenamehv[i]) == True:
        filenamehvo.append (filenamehv[i])
    if path.exists(filenamehh[i]) == True:
        filenamehho.append (filenamehh[i])

filename = filenamelo +filenamehho + filenamehvo
with open("outputlfile.csv", "wb") as f:
    writer = csv.writer(f)
    for l in filename:
        writer.writerow([l])

ftp.quit()