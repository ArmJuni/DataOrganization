'''
Created on Feb 27, 2018
Compare files from two directories, one internal and other external
If the file in the external file is not in the internal database the file will be copied
If the file exists this application  compare the dates and save the newest one keeping the old one in a backup folder
At the end it compress the Backup folder 

@author: arm.juni
'''
#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6
import shutil
import os.path
import datetime
from builtins import input        

#inputs of the paths for the directories to be compared and the backup folder
leftdir = input ("Provide the path to the folder with Planet output: ")
rightdir = input ("Provide the path to the folder with the data in use: ")
backup = input ("Provide the path where the backup folder will be created: ")

#Make a directory
def makedir (dirname):
    os.mkdir(dirname)

#4 - Function that compare files and copy newer files in the DB
def comparetime(lname,rname,fname):
    lpathfile = os.path.join(leftdir,fname,lname)
    rpathfile = os.path.join(rightdir,fname,rname)
    rpath = os.path.join(rightdir,fname)
    leftmtime = os.path.getmtime(lpathfile)
    rightmtime = os.path.getmtime(rpathfile)
    if leftmtime > rightmtime:
        copyfile(rpathfile,backupfolder)
        os.remove(rpathfile)
        copyfile(lpathfile,rpath)
        
#file to copy files from the external DB to the internal DB
def copyfile (origin,destination):
    shutil.copy2(origin,destination)
    
#3- create comparable names using XX_XXXX and file extension for an specific sub-folder
def comparenames (left,right,fname):
    #linst of files from the current DB to be used to verify if the file from the new Planet analysis is in the sub-folder 
    rlist = [ ]
    #Creating comparable names
    for l in left:
        lbasename = l.rsplit('_',1)[0]
        lsuffix = l.rsplit('.',1)[1]
        lcompname = lbasename + lsuffix
        lpathcn = os.path.join(leftdir,fname,l)
        rpathcn = os.path.join(rightdir,fname)
        for r in right:
            rbasename = r.rsplit('_',1)[0]
            rsuffix = r.rsplit('.',1)[1]
            rcompname = rbasename + rsuffix
            # If files are in the two databases call function comparetime
            if  lcompname == rcompname:
                comparetime(l,r,fname)
                #Create a list on internal files in this folder
                rlist.append(rcompname)
        # if files are not in the internal DB call function copyfile    
        if lcompname not in rlist:
            copyfile(lpathcn, rpathcn)
    rlist = [ ]

#compare folders in both DBs and create missing folders in current DB (rightfolder)
def comparefolder (lfolder, rfolder):
    for l in lfolder:
        if l not in rfolder:
            newdir = os.path.join(rightdir,l)
            makedir(newdir)  

#delete the backup folder            
def delete (pth):
    shutil.rmtree(pth)
    
#create the backup folder
today = datetime.datetime.now()
year = str(today.year)
month = str(today.month)
day = str(today.day)
hour = str(today.hour)
minute = str(today.minute)
backname = str(year + month + day + hour + minute)
backupcomplet = os.path.join(backup,backname)
makedir(backupcomplet)
backupfolder = (os.path.join (backup,backname))
print("Backup folder created: "+ backupfolder)  

#Make a list with the file names and extensions of each directory
leftfolders = os.listdir(leftdir)
rightfolders = os.listdir(rightdir)

#Call function 'Comparefolder'
comparefolder(leftfolders,rightfolders)

#Iterate through the folders
# 1 - iterate each folder from the Planet result (leftfolder) and from the current DB (rightfolder) creating a list of files in each variable from the same folder. 
for lf in leftfolders:
    leftfiles = os.listdir(os.path.join(leftdir,lf))
    #Criar um if para lidar com pasta vazia
    rightfiles = os.listdir(os.path.join(rightdir,lf))
    print ("Comparing folders: " + leftdir +"/" + lf + "/" + " and " + rightdir +"/" + lf + "/")
    # 2- call the function to compare the file names, sending as attributes the list of files and the specific sub-folder name 
    comparenames(leftfiles,rightfiles,lf)     
        
#Compress the Backup folder in Zip format 
compressed = os.path.join(backup,backname)       
shutil.make_archive(compressed, 'zip', backupfolder)
delete (backupfolder)
print("Comparison finished")