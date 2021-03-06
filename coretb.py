import datetime
import webbrowser
from tqdm import tqdm
import requests

url = "https://podaac-opendap.jpl.nasa.gov/opendap/allData/ghrsst/data/GDS2/L4/GLOB/JPL/MUR/v4.1/2019/006/20190106090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc.nc4?analysed_sst%5B0:1:0%5D%5B7904:1:9805%5D%5B7904:1:9805%5D"
url1 = "https://podaac-opendap.jpl.nasa.gov/opendap/allData/ghrsst/data/GDS2/L4/GLOB/JPL/MUR/v4.1"
url2 = "2019/006/20190106090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc.nc4?analysed_sst%5B0:1:0%5D%5B7904:1:9805%5D%5B7904:1:9805%5D"

x = datetime.date(2019, 1, 1)
n = 2
y19 = []
m19 = []
d19 = []
j19 = []

for i in range(n):
    dt = datetime.timedelta(i)
    y19.append((x + dt).year)
    m19.append((x + dt).month)
    d19.append((x + dt).day)
    j19.append((x + dt).strftime("%j"))

fname19 = []
for i in range(n):
    if m19[i]<10:
        m19[i] = "0" + str(m19[i])
    if d19[i]<10:
        d19[i] = "0" + str(d19[i])

    fname19.append(str(y19[i]) + str(m19[i]) + str(d19[i]) + 
    "090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc.nc4?analysed_sst%5B0:1:0%5D%5B7904:1:9805%5D%5B27173:1:32068%5D")
    
urls = []
for i in range(n):
    list1 = [url1, str(y19[i]), str(j19[i]), fname19[i]]
    str1 = "/".join(list1)
    urls.append(str1)

url = urls

for i in range(len(url)):
    r = requests.get(url[i], stream = True)
    total_size = int(requests.head(url[i]).headers['content-length'])
    #write-bin
    with open(str(y19[i]) + str(m19[i]) + str(d19[i]) + "-JPL-L4_GHRSST-Indonesia.nc4", 'wb') as f:
        for data in tqdm(iterable = r.iter_content(chunk_size= 1024), total = int(total_size/1024), unit = 'KB'):
            f.write(data)
    print(str(y19[i]) + str(m19[i]) + str(d19[i] +' Complete!'))
