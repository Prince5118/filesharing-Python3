from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from file.models import File,SharedRecord
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.views.static import serve
import os,hashlib
import shutil,random,string,subprocess
from io import StringIO
import mimetypes

from fus.settings import BASE_DIR,PROJECT_ROOT, SHARED_FOLDER,MEDIA_ROOT

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
import time 

# root/pjlogin/fus BASE_DIR
#/root/pjlogin/fus/Private/ SHARED_FOLDER

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

import cryptography
from cryptography.fernet import Fernet
import pyAesCrypt
from os import stat, remove
# key = b'1408' # Use one of the methods to get a key (it must be the same when decrypting)



from datetime import datetime as dt
from datetime import *

globalvariable = ''
logfile = os.path.join(PROJECT_ROOT,'linksharing.log')
mallogfile = os.path.join(PROJECT_ROOT,'malicious.log')

def genkey(c):
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(c))
    return x


def genhash(filepath):
    BLOCKSIZE =4096
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return (hasher.hexdigest())

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


# this will be used as a button next to download in home page
def sharefile(request):
    if request.user.is_authenticated:
                if request.method=='POST':
                   
                    user = User.objects.get(username=request.user.username)
                        # user is representing the sending user
                    files = user.files.all()
                #       users will represent all the available users he can send to ,so we can delete the name of sender from that list
                    users = [str(user) for user in User.objects.all()]
                    try:
                        selected_file = user.files.filter(name=request.POST['filename'])

                    except(KeyError):
                        return render(request,'file/home.html',{'error_message':"You DID NOT SELECT A FILE",})
                    else:
                        t = str(selected_file[0])
                        #t=t[18:]
                        #t=t[:-3]

                        # removes sender from the list
                        users = [str(u) for u in users if u != str(user)]
                        choices = ['1','10','30','60','1440']
                        #return HttpResponse(t)
                       # return render(request,'file/sharefile.html',{'t':t})
                        return render(request,'file/sharefile.html',{  
                        'nameoffile':t,
                        'sender':user,
                        'users':users,
                        'choicelist':choices,
                        })

                else :
                   # return render(request,'file/home.html',{'error_message':"You DID NOT SELECT A FILE method used was get",})
                     return render(request,'file/error_share.html')

    else:
        return redirect('file:login')


def userexpiry(request,nameoffile):
    if request.user.is_authenticated:
                if request.method=='POST':
                    bufferSize = 64 * 1024
                    global logfile
                    # list of recievers names
                    list_of_recievers = request.POST.getlist('recievers')

                    #expiry in minutes they selected
                    expiryminutes = request.POST.get('expirychoice')

                    #sender object
                    user = User.objects.get(username=request.user.username)

                    #selected file object
                    files = user.files.all()
                    selected_file = user.files.get(name=nameoffile)

                    # tells us original path and name of file
                    filepath = selected_file.path
                    ##'/home/prince/Pictures/file-3/fus/upload/user2/wood.jpg'
                    #dirname - /home/prince/Pictures/file-3/fus/upload/user2
                    #basename  - wood.jpg
                    display = ''
                   
                    
                    # Cant Share File greater then 250 mb
                    maxsize = 262144000
                    statinfo = os.stat(filepath) 
                    """
                    if int(statinfo.st_size)>maxsize:
                        return HttpResponse('You Cant Share File of size greater than 250 MegaBytes')
                    """
                    
                    #hash1 is hash value for file saved in user folder
                    hash1 = str(genhash(filepath))
                    hash2 = str(hashlib.sha256(filepath.encode()).hexdigest())
                    # Checking if the file shared already exists in SharedFOlder or not
                    # if it does then compare hash value to check if file in user folder has been tampered or not
                                     


                    flag = 0
                    sharedobj = SharedRecord.objects.filter(originalpath = filepath)
                    print(sharedobj)
                    for i in sharedobj:
                        if i.contenthash == hash1 and i.pathhash == hash2:
                            dst = i.copypath
                            print('here')
                            examplecopyname = i.copyname
                            keytobeused  = i.ekey
                            flag = 1
                            break
                       
                    #content changed of shared file compared to previous share
                   
                    # Updating immediately
                    #ext = nameoffile.split('.',1)[1]
                    src = filepath
                    dst1 = str(SHARED_FOLDER)

                    if not os.path.isdir(dst1):
                        os.makedirs(dst1)

                   
                    #randomstring = str(genkey(48))
                    if flag==0:
                        keytobeused = genkey(32)
                       
                        examplecopyname = str(genkey(48))+'.encrypted'
                        dst = str(SHARED_FOLDER) + examplecopyname
                        s = datetime.now()
                        with open(src, "rb") as fIn:
                        	with open(dst, "wb") as fOut:
                        		pyAesCrypt.encryptStream(fIn, fOut, keytobeused, bufferSize)
                       
                        os.chmod(dst,0o744)
                        e = datetime.now()
                        t = e - s
                        print('Encryption- ' + str(t))
              
                   
                    for item in list_of_recievers:
                        # Getting userrecord id for sender and reciever
                        temp = str(item)
                        # this variable contains expiry date of link
                        whentogo = datetime.now()+timedelta(minutes = int(expiryminutes))
                           
                        # object created as SharedRecord to be used in Sharing of File
                       
                        nameoflink = genkey(32)

                        obj = SharedRecord(originalpath=filepath,
                            copypath = dst,copyname =examplecopyname,
                            originalname=os.path.basename(filepath),shareddate=datetime.now(),
                            expirylength = expiryminutes,expirydate = whentogo,
                            contenthash = str(genhash(filepath)),pathhash = hashlib.sha256(filepath.encode()).hexdigest(),
                            sender = user.username,reciever = temp,
                            ekey = keytobeused,linkidentifier = nameoflink,linkpassword=genkey(8),
                            )
                        # obj.save() This line cut to last such that model is saved only after copying
                        obj.save()
                        
                        logtext = str(obj.shareddate.replace(microsecond=0))+' '+obj.sender+' Shared '+ obj.originalname  +' with '+obj.reciever        
                        write_log(logtext,logfile)
                       # hashedpassword = hashlib.md5(str(obj.ekey+obj.reciever).encode()).hexdigest()
                        display = display + '10.35.28.189:8000/'  + obj.linkidentifier +'---' + temp + '---'+ obj.linkpassword +"<br>"
                        #print(display)
                    

                    ###################
                    # email part should come here
                    #send_mail('<Your subject>', '<Your message>', 'from@example.com', ['wanisachin3@gmail.com'])
                    """
                    message = display
                    subject = 'Testing'
                    #from_email = settings.DEFAULT_FROM_EMAIL
                    from_email = 'LinkSharing'
                    to_email = ['wanisachin3@gmail.com']

                    send_mail(subject,message,from_email,to_email,fail_silently=False)
                    """
                    #################
                    return HttpResponse(display)

                else :
                    #request.method='GET'
                    # return render(request,'file/home.html',{'error_message':"You DID NOT SELECT A FILE method used was get",})
                     return render(request,'file/error_share.html')

    else:
        return redirect('file:login')
 
def testing(request,slug):    
    temp = SharedRecord.objects.filter(linkidentifier = str(slug))
    #x = temp[0]

    #Checkng if valid link
    if not temp:
        return HttpResponse('Invalid Link')

    #if viewed already
    x = temp[0]

    # if expiration date passed
    currentdate = datetime.now()
    isexpired = 0   
    viewed = 0

    if x.expirydate<currentdate:
        isexpired = 1
    if x.viewed==True:
        viewed = 1



    context = {'nameoflink':x.linkidentifier,'sharedobject':x,'linkcount':int(x.linkcount),
                'viewed':viewed,'isexpired':isexpired,'wrong':0}
    return render(request, 'file/Login_v1/askuser.html', context)


def filesharing(request):
    
    if request.method=='POST':
        
        global logfile
        global mallogfile
        
        requesting_user = request.POST['username']
    
        requesting_user = requesting_user.replace(" ", "")
    
        var = request.POST['nameoflink']
    
        entered_password = request.POST['hashedkey']
    
        temp = SharedRecord.objects.filter(linkidentifier = var)
        x = temp[0]

        #Autheticating the entered credentials
        wrong = 0

        
        if requesting_user.lower()!=x.reciever or entered_password!=x.linkpassword:
            # return to some error page saying you are not autheticated user
            # maybe increase authentication count like user tried 5 times or something
            wrong_attempt_datetime = datetime.now().replace(microsecond=0)
            bufferSize = 64 * 1024
            
            intcount = int(x.linkcount)
            intcount = intcount + 1
            x.linkcount = str(intcount)
            x.save()
            wrong = 1
            
            context = {'nameoflink':x.linkidentifier,'sharedobject':x,'linkcount':int(x.linkcount),
                'viewed':int(x.viewed),'isexpired':0,'wrong':wrong}
            
            #malicious attempt
            whyrejected = ''
            if requesting_user.lower()!=x.reciever and entered_password!=x.linkpassword:
                whyrejected = 'WrongID-Password'
            elif requesting_user.lower()!=x.reciever:
                whyrejected = 'WrongID'
            else :
                whyrejected = 'WrongPassword'
            # date time linkname sender filename intendedreciever attemptedby whyrejected wrongattemptcount
            logcontent = str(wrong_attempt_datetime)+ ' '+x.linkidentifier+' '+ x.sender + ' '+ x.originalname+' '+x.reciever+' '+requesting_user+' '+whyrejected+' '+x.linkcount
            write_log(logcontent,mallogfile)

            return render(request, 'file/Login_v1/askuser.html', context)



        # if expiration date passed
        currentdate = datetime.now()
        if x.expirydate<currentdate:
            return HttpResponse('Link Expired')  
        
        
        linkidentifier = x.linkidentifier
        copyname = x.copyname
        copypath = x.copypath
        originalname = x.originalname
        sender = x.sender 
        reciever = x.reciever
     
        typeofmime = str(mimetypes.MimeTypes().guess_type(originalname)[0])
        key = x.ekey

        ###########
        #Decryption and logging 

        
        start = datetime.now()
        encFileSize = stat(copypath).st_size
        outputfile = copypath+'pj'
        bufferSize = 64*1024
        
        with open(copypath, "rb") as fIn:
	        with open(outputfile, "wb") as fOut:
		        try:
                            pyAesCrypt.decryptStream(fIn, fOut, key, bufferSize, encFileSize)
                            #encrypted = fOut.read()
			# decrypt file stream
			   # pyAesCrypt.decryptStream(fIn, fOut, key, bufferSize, encFileSize)
                           # encrypted = fOut.read()
                         
		        except ValueError:
                            remove(copypath)

			# remove output file on error
#			  remove(encfile)

        end = datetime.now()
        timetaken = end-start
        print('Time Decryption: ',timetaken) 

        logtext = str(datetime.now().replace(microsecond=0))+' '+reciever + ' accessed ' + originalname + ' sharedby '+sender
        write_log(logtext,logfile)    

        with open(outputfile,"rb") as f:
            encrypted = f.read()
        remove(outputfile)
        end = datetime.now()
        timetaken = end-start
        print('Time Decryption: ',timetaken) 

        response = HttpResponse(encrypted)
        response['Content-Type'] = typeofmime
        response['Content-Disposition'] = 'attachment; filename= "{}"'.format(originalname)
        x.viewed=True
        x.save()
        return response

        return HttpResponseRedirect('') 
    
    else:
        return HttpResponse("Unsupported method Please use GET or POST ", status=405)

# Function for admin home page


def uadmin(request):
    if request.user.is_authenticated and request.method == 'GET' and request.user.username=='admin':
        global logfile
        global mallogfile 
        with open(logfile, 'r') as f:
            lines = [line.rstrip('\n').split(' ') for line in f]
        
        lines = lines[:1000]
 
        page = request.GET.get('page', 1)

        paginator = Paginator(lines, 30)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
             
            #2019-06-21 12:43:22.363334 user1 Shared user1_readme.txt with admin
            #2019-06-21 12:44:55.697242 admin accessed user1_readme.txt sharedby user1
        with open(mallogfile,'r') as f:
            lines = [line.rstrip('\n').split(' ') for line in f]
             
        
        
        page = request.GET.get('page', 1)

        paginator = Paginator(lines, 9)
        try:
            malicious_data = paginator.page(page)
        except PageNotAnInteger:
            malicious_data = paginator.page(1)
        except EmptyPage:
            malicious_data = paginator.page(paginator.num_pages)

        #listofuser 
        countofuser = User.objects.all().count()
        alluser = User.objects.all()
        listofuser = [str(item) for item in alluser]

        context = {'data':data,'malicious_data':malicious_data,'listofuser':listofuser,'countofuser':countofuser}

        return render(request, 'file/uadmin.html', context)

    else:
        return HttpResponse('Wrong')

def fetch(request):
    if request.user.is_authenticated  and request.user.username=='admin' :
        if request.method=="POST":
            x = request.POST['nameofuser']
            var = '/uadmin/view='+str(x)
            return HttpResponseRedirect(var)
        else:
            return HttpResponse("Unsupported method Please use GET or POST ", status=405)
    else:
        return HttpResponseRedirect('')




# Specific User Search Request
def specificuser(request,slug):
    if request.user.is_authenticated  and request.user.username=='admin' :
        x = slug
        global logfile
        global mallogfile 
        listofrecord = []
        with open(logfile, 'r') as f:
            for line in f:
                if re.search(x, line):
                    line = line[:-1]# remving /n character
                    line = line.split(' ')
                    listofrecord.append(line)

        


        page = request.GET.get('page', 1)

        paginator = Paginator(listofrecord, 15)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)


        return render(request, 'file/specificuser.html', {'data':data})

    #2019-06-21 12:43:22.363334 user1 Shared user1_readme.txt with admin
    #2019-06-21 12:44:55.697242 admin accessed user1_readme.txt sharedby user1
    # username is 2nd and 6th index

    else:
        return HttpResponseRedirect('')



