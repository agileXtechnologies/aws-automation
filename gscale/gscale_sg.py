#!/usr/bin/env python
# coding: utf-8

# In[5]:


import platform, subprocess, os, time, random, json
    
def errorCheck(check,prot):
    if check[0] != 0:
        print("[⛏] Error With {0} Key: ".format(prot))
        print(check[1])
        print("[🔐] Please enter it correctly next time")
        return True
    else:
        return False
       
def gscaleSecurityGroup():
    if platform.system() == 'Windows':
        os.system("cls")
    else:
        os.system("clear")
    print("[*] Creating Firewall...")
    time.sleep(2)
    groupName= input("[.] Group Name: ")
    rint= random.randint(0,100000)
    groupName= groupName+str(rint)
    print("[*] Creating {0} security group".format(groupName))
    sg= subprocess.getstatusoutput('aws ec2 create-security-group --description "gscale-security-group" --group-name "{0}"'.format(groupName))
    print("[✔] {0} Security group created".format(groupName))
    print("[*] Allowing SSH:22 ...")
    portSSH= subprocess.getstatusoutput('aws ec2 authorize-security-group-ingress --group-name {0} --protocol tcp --port 22 --cidr 0.0.0.0/0'.format(groupName))
    print("[✔] SSH Allowed...")
    print("[*] Allowing HTTPD:80 ...")
    portSSH= subprocess.getstatusoutput('aws ec2 authorize-security-group-ingress --group-name {0} --protocol tcp --port 80 --cidr 0.0.0.0/0'.format(groupName))
    if input("[?] Do you want any other service port to be running? (y/n)") == "y":
        newPort= input("[.] Enter the port number: ")
        newProto= input("[.] Enter the protocol: ")
        newCIDR= input("[.] Enter the CIDR for allowed connection: ")
        print("[*] Allowing {0} on {1}:{2}".format(newCIDR,newProto,newPort))
        newIngress= subprocess.getstatusoutput('aws ec2 authorize-security-group-ingress --group-name {0} --protocol {1} --port {2} --cidr {3}'.format(groupName,newProto,newPort,newCIDR))
        if errorCheck(newIngress,"port|protocol|CIDR"):
            exit()
        else:
            print("[✔] Allowed {0} on {1}:{2}".format(newCIDR,newProto,newPort))
            print("[✔] Creation of Firewall done")
    else:
        print("[✔] Creation of Firewall done")
        
    sgJson= json.loads(sg[1])
    sgID= sgJson["GroupId"]
    return sgID






