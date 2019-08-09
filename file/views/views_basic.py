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

# root/pjlogin/fus BASE_DIR
#/root/pjlogin/fus/Private/ SHARED_FOLDER

from datetime import datetime as dt
from datetime import *

def genkey(c):
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(c))
    return x


def home(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        files = user.files.all()
        paginator = Paginator(files, 5)
        page = request.GET.get('page')
        #return HttpResponse(MEDIA_ROOT)


        if not os.path.isdir(SHARED_FOLDER):
            os.makedirs(SHARED_FOLDER)

        if bool(files):
            files = paginator.get_page(page)
            context = {'paginator': paginator,
                       'files': files,
                       'user': user,
                      }
            return render(request, 'file/home.html', context, status=200)
        else:
            context = {'warn_msg': '''You haven't Uploaded any
                                Files just upload some files to access it''',
                        }
            return render(request, 'file/home.html', context, status=200)
    else:
        return  redirect('file:login')


def log_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    else:
        if request.method == 'GET':
            form = AuthenticationForm()
            return render(request, 'file/Login_v1/index.html', {'form': form}, status=200)
        elif request.method == 'POST':
            #form = AuthenticationForm(data=request.POST)
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                #return HttpResponseRedirect("/")
                x = form.get_user()
                t = str(x)
                if t=='admin':
                    return HttpResponseRedirect("/uadmin")
                else:
                    return HttpResponseRedirect("/")

            else:
                return render(request, 'file/Login_v1/index.html', {'form': form}, status=200)
        else:
            return HttpResponse("Unsupported method Please use GET or POST ", status=405)




def upload(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'file/upload.html', status=200)
        if request.method == 'POST':
            try:
                file_name, file_path = handle_uploaded_file(request, request.FILES['file'], str(request.FILES['file']))
                #return HttpResponse(file_path)
                # when user2 uploaded file it showed filepath to be /root/pjlogin/fus/upload/user2/readme.md
                #  return HttpResponse(SHARED_FOLDER)
                filevar = File(name=file_name, user=request.user, path=file_path)
                filevar.save()
                return HttpResponseRedirect("/")
            except KeyError:
                return HttpResponseRedirect("/upload")
            except ValueError:
                return HttpResponse("File Already Exists", status=400)
        else:
            return HttpResponse("Unsupported method Please use GET or POST ", status=405)
    else:
        return HttpResponseRedirect("/login")

def handle_uploaded_file(request, file, filename):
    user_name = request.user.username

    filename = str(filename)

    #filename = str(user_name)+'_'+filename

    path = 'upload/{}/'.format(request.user.username) + filename

    if os.path.exists(path):
        return HttpResponse("File Already Exists", status=200)
    if not os.path.exists('upload/'):
        os.mkdir('upload/')
    if not os.path.exists('upload/{}/'.format(user_name)):
        os.mkdir('upload/{}/'.format(user_name))
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    abs_path = os.path.abspath(path)
    return filename, abs_path


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'file/signup.html', {'form': form}, status=200)
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        emailid = request.POST['emailid']

        if not form.is_valid():
            return render(request, 'file/signup.html', {'form': form}, status=200)
        form.save()
        user = User.objects.get(username=form.cleaned_data.get('username'))
        user.email = emailid
        user.save()
        login(request, user)
        return HttpResponseRedirect("/login")
    else:
        return HttpResponse("Unsupported method Please use GET or POST ", status=405)



def log_out(request):
    if request.method=='GET':
        logout(request)
        return HttpResponseRedirect("/login")
    else :
        return HttpResponse("Unsupported method Please use GET or POST ", status=405)


def download(request):
    if request.user.is_authenticated:        
        user = User.objects.get(username=request.user.username)
        files = user.files.all()

        try:
                selected_file = user.files.filter(name=request.POST['filename'])


        except(KeyError):
            render(request,'file/home.html',{'error_message':"You DID NOT SELECT A FILE",})
       
        else:
           
            t = selected_file[0]

            typeofmime = str(mimetypes.MimeTypes().guess_type('t.name')[0])

            filespath = t.path
            p = open(filespath,'rb').read()

            response = HttpResponse(p)
            response['Content-Type'] = typeofmime
            response['Content-Disposition'] = 'attachment; filename= "{}"'.format(t.name)  
            return response
