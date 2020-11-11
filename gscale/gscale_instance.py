#!/usr/bin/env python
# coding: utf-8

# In[3]:


import platform, subprocess, os, time, random, json
    
def errorCheck(check,prot):
    if check[0] != 0:
        print("[⛏] Error With {0} Key: ".format(prot))
        print(check[1])
        print("[🔐] Please enter it correctly next time")
        return True
    else:
        return False
    
def checkInsState(instId):
    print("[*] Checking Instance State...")
    while(True):
        descIns= subprocess.getstatusoutput('aws ec2 describe-instances --instance-ids {0}'.format(instId))
        descInsJson= json.loads(descIns[1])
        insState= descInsJson["Reservations"][0]["Instances"][0]["State"]["Name"]
        if insState == "running":
            print("[✔] Instance Running")
            break
            
def okStatusCheck(instaId):
    print("[*] Checking Instance Status...")
    os.system('aws ec2 wait instance-status-ok --instance-ids {0}'.format(instaId))
    print("[✔] Instance status OK")
    
def gscaleInstance(secuGroup):
    if platform.system() == 'Windows':
        os.system("cls")
    else:
        os.system("clear")
    print("[*] Launching Instance and Server Configuring")
    time.sleep(1)
    print("[*] Launching Instance...")
    time.sleep(1)
    keyName= input("[.] Enter Key Name to use: ")
    lauInst= subprocess.getstatusoutput("aws ec2 run-instances --image-id ami-052c08d70def0ac62 --count 1 --instance-type t2.micro --key-name {0} --security-group-id {1}".format(keyName,secuGroup))
    print("[✔] Instance launched with key: {0} and security-group: {1}".format(keyName,secuGroup))
    print("[*] Creating EBS Volume...")
    ebsSize= input("[.] Enter the size in GB: ")
    ebsType= input("[.] Enter the Type of Volume: ")
    insJson= json.loads(lauInst[1])
    insID= insJson["Instances"][0]["InstanceId"]
    insAz= insJson["Instances"][0]["Placement"]["AvailabilityZone"]
    ebsCreate= subprocess.getstatusoutput("aws ec2 create-volume --volume-type {0} --size {1} --availability-zone {2}".format(ebsType,ebsSize,insAz))
    if errorCheck(ebsCreate,"Volume Type|Size"):
        exit()
    else:
        print("[✔] EBS Volume created")
    checkInsState(insID)
    okStatusCheck(insID)
    print("[*] Attaching EBS Volume...")
    ebsJson= json.loads(ebsCreate[1])
    volID= ebsJson["VolumeId"]
    ebsAttach= subprocess.getstatusoutput('aws ec2 attach-volume --volume-id {0} --instance-id {1} --device /dev/sdf'.format(volID,insID))
    print("[✔] EBS Volume Attached")
    print("[*] Configuring Instance")
    insPubIP= subprocess.getoutput('aws ec2 describe-instances --query "Reservations[*].Instances[*].PublicIpAddress" --output text')
    print("[*] Formatting Device...")
    insForm= subprocess.getstatusoutput('ssh -i {0}.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ec2-user@{1}  "sudo mkfs.ext4 /dev/xvdf"'.format(keyName,insPubIP))
    print("[✔] Formated device")
    print("[*] Installing Apache Webserver...")
    insHttpd= subprocess.getstatusoutput('ssh -i {0}.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ec2-user@{1}  "sudo yum install httpd -y"'.format(keyName,insPubIP))
    print("[✔] Apache Webserver Installed")
    print("[*] Mounting Device to /var/www/html")
    insMount= subprocess.getstatusoutput('ssh -i {0}.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ec2-user@{1}  "sudo mount /dev/xvdf /var/www/html"'.format(keyName,insPubIP))
    print("[✔] Mounted Device")
    print("[*] Starting httpd service...")
    insHttpdStart= subprocess.getstatusoutput('ssh -i {0}.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ec2-user@{1}  "sudo systemctl start httpd"'.format(keyName,insPubIP))
    print("[✔] Httpd Service started")
    print("[*] Enableing httpd service...")
    insHttpdEnable= subprocess.getstatusoutput('ssh -i {0}.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ec2-user@{0}  "sudo systemctl enable httpd"'.format(keyName,insPubIP))
    print("[✔] Httpd Service enabled")
    print("[*] Installing git...")
    insGit= subprocess.getstatusoutput('ssh -i {0}.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ec2-user@{1}  "sudo yum install git -y"'.format(keyName,insPubIP))
    print("[✔] git installed")
    os.system("sudo setenforce 0")
    print("[✔] Configured Instance")
    return keyName,insPubIP
    
    


