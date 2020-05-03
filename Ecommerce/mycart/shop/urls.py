from django.contrib import admin
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
# from .views import GeneratePdf

urlpatterns = [
 path('', views.about,name="about"),
 path('login/',views.login,name="login"),
 path('newaccount/',views.newaccount,name="newaccount"),
 path('logout1/',views.logout1,name="logout1"),
 path('social/',views.social,name="social"),
 path('sociallogout/',views.sociallogout,name="sociallogout"),
 path("logout/", auth_views.LogoutView.as_view(), name="logout"),
 path('addcart/<int:id1>/',views.addcart,name="addcart"),
 path('proddesc/<int:id2>/',views.proddesc,name="proddesc"),
 path('Bynow/<int:id3>/',views.Bynow,name="Bynow"),
 path('Zoom/<int:id4>/',views.Zoom,name="Zoom"),
 path('search/',views.search,name="search"),
 path('filter/',views.filter,name="filter"),
 path('showcart/',views.showcart,name="showcart"),
 path('deletecart/<int:id4>/',views.deletecart,name="deletecart"),
 path('dashbord/',views.dashbord,name="dashbord"),
 path('varification/',views.varification,name="varification"),
 path('change/',views.change,name="change"),
 path('delete/<int:id5>/',views.deleteorder,name="deleteorder"),
 path('reating/',views.reating,name="reating"),
 path('chageaccount/',views.chageaccount,name="chageaccount"),
 path('Feedback/',views.Feedback,name="Feedback"),
 path('addaddress/',views.addaddress,name="addaddress"),
 path('changeaddress/',views.changeaddress,name="changeaddress"),
 path('multiorder/',views.multiorder,name="multiorder"),
 path('morediscount/',views.morediscount,name="morediscount"),
 path('premimum/',views.premimum,name="premimum"),
 path('moreselling/',views.moreselling,name="moreselling"),
 path('payment/',views.payment,name="payment"),
 path('handlerequest1/',views.handlerequest1,name="HandleRequest1"),
 path('handlerequest2/',views.handlerequest2,name="HandleRequest2"),
#  path('pdf/',GeneratePdf.as_view(),name="pdf"),
 path('pdfdownload/',views.pdfdownload,name="pdfdownload"),
 path('multiordercreate/',views.multiordercreate,name="multiordercreate"),
 path('oneorder/',views.oneorder,name='oneorder'),
]