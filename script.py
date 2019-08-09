#!/root/pjlogin/fus-3/bin/python

import shutil
from os import listdir
from os.path import isfile, join
import os
import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fus.settings")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fus.settings")
django.setup()

from crontab import CronTab


from file.models import User,SharedRecord,File
from fus.settings import BASE_DIR,PROJECT_ROOT, SHARED_FOLDER,MEDIA_ROOT

from datetime import datetime


def write_log(text, logfile):
        #We read the existing text from file in READ mode
    f=open(logfile,"r")
    fline=text + "\n"    #Prepending string
    oline=f.readlines()
    #Here, we prepend the string we want to on first line
    oline.insert(0,fline)
    f.close()
     
     
    #We again open the file in WRITE mode 
    src=open(logfile,"w")
    src.writelines(oline)
    src.close()
    return


temp = SharedRecord.objects.all()

#DELETING FOLDERS
folder = SHARED_FOLDER
#subfolders = [ f for f  in os.scandir(folder)]
#print(subfolders)
onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

#deleting Shared Records
now = datetime.now()
print(str(now))


logfile = os.path.join(PROJECT_ROOT,'linksharing.log')

for item in temp:
    if item.expirydate<datetime.now():
        print('deleting a sharedrecord')
        now = datetime.now()
        now = now.replace(microsecond=0)
        text1 = ''
        now = str(now)
        text1 += now+' '+item.sender+' Deleted_SharedRecord '+item.originalname +' '+str(item.shareddate.date())+'_'+str(item.shareddate.time().replace(microsecond=0))+' '+item.reciever
        write_log(text1,logfile)
        item.delete()


#deleting files
for item in onlyfiles:   
    
    flag = 0
    
    # flag 0 means its currently not used in any sharedrecord
    for record in temp:
        if record.copyname==str(item):
            flag=1
            # d = SHARED_FOLDER + item
    d = SHARED_FOLDER + item
    if flag==0:
        
       # item = SharedRecord.objects.filter(copyname=str(item))
        #item = item[0]
        print(d)
        os.remove(d)
        text = str(now.replace(microsecond=0))+' '+'System'+' Deleted_File '+item+' '+'-'+' '+'-'
        write_log(text,logfile)
        #shutil.rmtree(d)




