from django.urls import path, re_path
from . import views

app_name = 'file'

urlpatterns = [
    path('', views.home, name='home'),
    path('uadmin',views.uadmin,name='uadmin'),

    path('sharefile',views.sharefile,name='sharefile'),
    path('download',views.download,name='download'),

    path('login', views.log_in, name='login'),
    path('upload', views.upload, name='upload'),
    path('signup', views.signup, name='signup'),
    path('logout', views.log_out, name='logout'),

    path('filesharing', views.filesharing, name='filesharing'),

    re_path(r'userexpiry/(?P<nameoffile>.*)/', views.userexpiry,
name='userexpiry'),    

    re_path(r'(?P<slug>.{32})/',views.testing,name = 'testing'),

    re_path(r'uadmin/specificuser/',views.fetch,name = 'fetch'),

    re_path(r'uadmin/view=(?P<slug>.*)/',views.specificuser,name = 'specificuser')
   
]