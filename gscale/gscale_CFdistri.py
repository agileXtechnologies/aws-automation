#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import platform, subprocess, os, time, random, json
def errorCheck(check,prot):
    if check[0] != 0:
        print("[⛏] Error With {0} Key: ".format(prot))
        print(check[1])
        print("[🔐] Please enter it correctly next time")
        return True
    else:
        return False
    
def gscaleCF(keyName,insPubIp):
    distriList= []
    print("[*] Creating S3 Bucket...")
    time.sleep(1)
    buckName= input("Enter unique name for bucket: ")
    buckCreate= subprocess.getstatusoutput('aws s3api create-bucket --bucket {0} --acl public-read-write --region us-east-1'.format(buckName))
    if errorCheck(buckCreate,"S3 Bucket"):
        exit()
    else:
        print("[✔] S3 Bucket Created")
    print("[*] Adding objects to bucket...")
    num= int(input("Enter number of objects to add: "))
    for i in range(0,num):
        print("[*] Uploading object {0}".format(i+1))
        objPath= input("Enter the local path of the object: ")
        objLoc= input("Enter the location of object in bucket: ")
        buckUpload= subprocess.getstatusoutput('aws s3api put-object --acl public-read-write --bucket {0} --key {1} --body {2}'.format(buckName,objLoc,objPath))
        print("[✔] Uploaded object {0}".format(i+1))
    print("[✔] Objects Added to Bucket")
    print("[*] Creating CloudFront Distribution")
    no= int(input("Enter the number of objects to be distributed: "))
    for i in range(0,no):
        print("[*] Creating Distri {0}".format(i+1))
        cfObject= input("Enter the location of object in bucket: ")
        cfCreate= subprocess.getstatusoutput('aws cloudfront create-distribution --origin-domain-name {0}.s3.amazonaws.com --default-root-object {1}'.format(buckName,cfObject))
        cfJson= json.loads(cfCreate[1])
        domain= cfJson["Distribution"]["DomainName"]
        distriId= cfJson["Distribution"]["Id"]
        distriList.append(distriId)
        print("Edit this link in your code and push it in GitHub")
        print(domain)
        print("[✔] Distri {0} created".format(i+1))
    print("[✔] Created CloudFront Distribution")
    print("[*] CloudFront is coming up...")
    os.system("aws cloudfront wait --id {0}".format(distriList[-1]))
    print("[✔] CloudFront is up")
    time.sleep(1)
    input("Press any key after editing your code with cloudfront link to continue further...")
    print("[*] Uploading code to Instance")
    gitUrl= input("Enter the Git URL :")
    insCodeUpload= subprocess.getstatusoutput('ssh -i {0}.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ec2-user@{1}  "sudo git clone {2}"'.format(keyName,insPubIp,gitUrl))
    insCodeCopy= subprocess.getstatusoutput('ssh -i {0}.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ec2-user@{1}  "sudo cp gscale/index.html /var/www/html/"'.format(keyName,insPubIp))
    print("[✔] Uploaded Code to Instance")
    os.system('"ssh -i {0}.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ec2-user@{1}  "sudo setenforce 0"'.format(keyName,insPubIp))
    print("Access your website on {0}/<page name>".format(insPubIp))
    
    
        


# In[ ]:




