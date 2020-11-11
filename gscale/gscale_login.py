#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import subprocess, time, os, getpass, pyfiglet
def gscaleLogin():
    count= 0
    print("------------------------------------------------------")
    ascii_banner = pyfiglet.figlet_format("gscale\nGlobal Scale")
    print(ascii_banner)
    print("------------------------------------------------------")
    print("\ngscale is built on AWS CloudFront for scaling your appliction automatically and with ease.\nIt is in beta phase of development. You can smoothly scale Web Application on Apache(Httpd) Webserver\nNOTE: This will charge you money!")
    print("You should have a AWS Account for using this tool")
    print("Author: Shubham Bhalala")
    print("Reach me out @ https://www.linkedin.com/in/shubham-bhalala-a5062916b/")
    print("\n[*] Starting gscale...")
    time.sleep(2)
    print("[✔] gscale started...")
    print("[*] AWS Configure...")
    accKey= getpass.getpass("[.] AWS Access Key ID: ")
    secKey= getpass.getpass("[.] AWS Secret Access Key: ")
    defRegion= input("[.] Default region name: ")
    confAccKey= subprocess.getstatusoutput("aws configure set aws_access_key_id {0}".format(accKey))
    confSecKey= subprocess.getstatusoutput("aws configure set aws_secret_access_key {0}".format(secKey))
    confRegion= subprocess.getstatusoutput("aws configure set default.region {0}".format(defRegion))
    if confAccKey[0] == 0:
        print("[✔] Access Key Entered")
        print(confAccKey[1])
        count= count +1
    else:
        print("[⛏] Error With Access Key: ")
        print(confAccKey[1])
        print("[🔐] Please enter it correctly next time")
        #accKey= input("[.] AWS Access Key ID: ")
        #confAccKey= subprocess.getoutput("aws configure set aws_access_key_id {0}".format(accKey))
    if confSecKey[0] == 0:
        print("[✔] Secret Access Key Entered")
        print(confSecKey[1])
        count= count +1
    else:
        print("[⛏] Error With Secret Access Key: ")
        print(confSecKey[1])
        print("[🔐] Please enter it correctly next time")
        #secKey= input("[.] AWS Secret Access Key: ")
        #confSecKey= subprocess.getoutput("aws configure set aws_secret_access_key {0}".format(secKey))
    if confRegion[0] == 0:
        print("[✔] Region Entered")
        print(confRegion[1])
        count= count +1
    else:
        print("[⛏] Error With Default Region Key: ")
        print(confRegion[1])
        print("[🔐] Please enter it correctly next time")
        #defRegion= input("[.] Default region name: ")
        #confRegion= subprocess.getoutput("aws configure set default.region {0}".format(defRegion))
    if count == 3:
        return True
    else:
        return False







