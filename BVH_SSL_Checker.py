#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Extract Links from BVH Site
# Run only one time to get the newest ULRs

import requests
from bs4 import BeautifulSoup
import re

bvh = "https://www.bvh.org/mitgliedsvereine/"
response = requests.get(bvh)
if response.status_code == 200:
    
    soup = BeautifulSoup(response.text, "html.parser")
    
links = []

for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
    links.append(link.get('href'))
    
for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
    links.append(link.get('href'))
    


# In[ ]:


# Clean extracted Links

links_optimized = []
  
for item in links:
        requests.get(item, verify=True)
        
        if item.count('https')>0:
            item = item[8:]
        if item.count('http')>0:
            item = item[7:]
        if item.count('www.')>0:
            item = item[4:]
        if item.endswith("/"):
            item = item.rstrip("/")
       
    
        if item not in links_optimized and not item.count('bvh.org')>0 and not item.count('facebook')>0         and not item.count('instagram')>0 and not item.count('linkedin')>0 and not item.count('youtube')>0 and not item.count('xing')>0:
            links_optimized.append(item)
                
print(links_optimized)


# In[ ]:


# Count URLs

print(len(links_optimized))


# In[ ]:


# SSL checker - Notebook Output

def https_checkup(item):
        URL = 'https://' + item
        response = requests.get(URL, verify=True)
        if response.status_code == 200:
            print(item + " OK")
        else:
            print(item + " SSL Inconsistency")
            
for item in links_optimized:
    try:
        https_checkup(item)
    except:
        print(item + " Error / No SSL Cert found!")
        pass


# In[ ]:


# SSL checker - CSV Output
import csv
import datetime


    
date = datetime.date.today()

def https_checkup_log(item):
    URL = 'https://' + item
    response = requests.get(URL, verify=True)
    if response.status_code == 200:
        csv_writer.writerow([item, "OK", str(date)])
    else:
        csv_writer.writerow([item, "SSL Error", str(date)])
            
            
            
with open("bvh_audit.csv","a") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["URL", "Status", str(date)])            
            
    for item in links_optimized:
        try:
            https_checkup_log(item)
        except:
            csv_writer.writerow([item, "No SSL Cert found", str(date)])
        pass
    
f.close()


# In[ ]:


# Check single site  SSL Status
requests.get('https://hofer-boersenforum.de')


# In[ ]:


# Detailed Cert Analysis

from urllib.request import Request, urlopen, ssl, socket
from urllib.error import URLError, HTTPError
import json

#some site without http/https in the path
base_urls = links_optimized
port = '443'

for base_url in base_urls:
    hostname = base_url
    context = ssl.create_default_context()
    
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())
            data = json.dumps(ssock.getpeercert())
            # print(ssock.getpeercert())
            
    print (base_url + " SSL Cert: ")

    print (data)

