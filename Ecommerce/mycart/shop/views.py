from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages 
from django.contrib.sessions.models import Session
from .models import user, product,address,userorder,countery,state,District,product_rating,feedback,orderdelete
from math import ceil
import datetime
from django.db.models import Q
from django.db.models import Max,Min
from django.core.mail import send_mail 
import random
from django.contrib.auth.models import User,auth

import requests
import json

from decouple import config

from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
# Pdf code-------------------------------------
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf #created in step 4
from social_django.models import UserSocialAuth
# passlib
from passlib.hash import sha256_crypt

# --------------------------------------pip install python-decouple------------------------

MID=config('MID')
MERCHANT_KEY=config('MERCHANT_KEY')
GOOGLE_RECAPTCHA_SECRET_KEY=config('captcha_secret')
# Create your views here.
def about(request):
    products = product.objects.all()
    # [0:6]
    if request.session.has_key('is_loged'):
       userid=request.session.get('is_loged')
       username=request.session.get('is_name')
       userstr=str(userid)
       cartid=request.session.get(userstr)
       if cartid:
           n=len(cartid)
       else:
           n=0
       params = {'login':'YES','product': products,'lenth':n,'name':username}       
       return render(request,'index.html',params)
    else:
       n=0
       params = {'login':'','product': products,'lenth':n}
       return render(request,'index.html',params)

# Login
def login(request):
    if request.method =='POST':
      email=request.POST['email']
      password=request.POST['password']
      if user.objects.filter(email=email).exists():
         u=user.objects.filter(email=email)
         for temp in u:
            print(temp.id)
         password2=temp.password
         if sha256_crypt.verify(password,password2):
             request.session['is_loged']=temp.id
             request.session['is_name']=temp.name
             print(request.session['is_loged'])
             return redirect("about")
         else:
             messages.add_message(request,messages.ERROR,"Invalid Password")
             return redirect("login")
      else:
        messages.add_message(request,messages.ERROR,"Invalid Email")
        return redirect("login")
    else:
        return render(request,"login.html")
     
# New Account
# pip install passlib

def newaccount(request):     
    if request.method=='POST':
        name=request.POST['user']
        email=request.POST['email']
        password=request.POST['password']
        print(email)
        if user.objects.filter(email=email).exists():
            messages.info(request,"User is alredy exists")
            return redirect("newaccount")
        else:
            params={'name':name,'Email':email,'password':password}
            n=random.randint(1000,5000)
            request.session['varification']=n 
            request.session['email']=email
            mail=send_mail("Varifcation code of Mycart","Please Enter Varification code","ayadavupc@gmail.com",[email],fail_silently=False,html_message='''<h2>Your Email is {} and Varification code is {}</h2>'''.format(email,n))
            if mail:
              return render(request,"varificartion.html",params)  
            else:
                messages.error(request,"Some Problem occur in sending varification code Sorry !! ")     
        
    return render(request,"newaccount.html")  
        
# Varification Code
def varification(request):
    if request.method == "POST" :
        code=request.POST['verify']
        code=int(code)
        password=request.POST.get('password')
        username=request.POST.get('user')
        n=request.session.get('varification')
        Email=request.session.get('email')
        del request.session['email']
        del request.session['varification']
        print(Email,code,password,username)
        if code==n:
            # password = bytes("sasd7823%^#%$#%^#%hdjfdfgjhdgdNNVVVV"+password+"qwertzxcvghjk5678!&56#*as(?)@87654asdfgh", 'utf-8')
            password=password=sha256_crypt.hash(password)
            obj=user(name=username,email=Email,password=password)
            obj.save()
            messages.info(request,"You are registered successfull")
            return redirect("login")
        else:
            messages.error(request,"Not match verification code")     
            return redirect("newaccount")
    return render(request,"newaccount.html")

# Logout
def logout1(request):
   del request.session['is_loged']
   del request.session['is_name']
   if 'pro_id' in request.session:
    del request.session['pro_id']
   return redirect('login')

# Social account login 

def social(request):
    socialuser=request.user
    if socialuser.is_authenticated:
        if socialuser.social_auth.filter(provider='google-oauth2'):
            print ('user is using Google Account!')
            u=socialuser.social_auth.filter(provider='google-oauth2')
            temp1=0
            temp2=0
            for i in u:
                temp1=i
            userobj=user.objects.filter(email=temp1.uid)
            print(userobj)
            for i in userobj:
                temp2=i
            request.session['is_loged']=temp2.id
            request.session['is_name']=temp2.name
            messages.info(request,"you are login with google successfull")
            print(temp1.uid)
            print((temp1.user).username)   
        # elif socialuser.social_auth.filter(provider='facebook-oAuth2'):
        #     print ('user is using Google Account!')
        #     u=socialuser.social_auth.filter(provider='facebook-oAuth2')
        #     temp1=0
        #     temp2=0
        #     for i in u:
        #         temp1=i
        #     userobj=user.objects.filter(email=temp1.uid)
        #     for i in userobj:
        #         temp2=i
        #     request.session['is_loged']=temp2.id
        #     request.session['is_name']=temp2.name
        #     messages.info(request,"you are login with Facebook successfull")
        #     # print(i.uid)
        #     # print((i.user).username)             
        else:
            messages.error(request,"Something is worng !")
    return redirect("about")

# Social logout 
def sociallogout(request):
    if 'is_loged' in request.session:
        del request.session['is_loged']
    if 'is_name' in request.session:    
        del request.session['is_name']
    if 'pro_id' in request.session:
        del request.session['pro_id']
    return redirect('login')

# Chage Password
def change(request):

    if request.method =='POST':
        Email=request.POST['Email']
        newpassword=request.POST['Password']
        newpassword2 = password=password=sha256_crypt.hash(newpassword2)
        temp=''
        if user.objects.filter(email=Email).exists():
            userobj=user.objects.filter(email=Email)
            for i in userobj:
                temp=i
            temp.password=newpassword2
            temp.save()
            mail=send_mail("Password Change of Mycart","Your Password Change Successfully","ayadavupc@gmail.com",[Email],fail_silently=False,html_message='''<h3>Your Email is {} and New Password  is {} Password Change aney Query Please Contect me {}</h3>'''.format(Email,newpassword,8318167080))
            if mail:
              messages.info(request,"Your Password Successfully Change")
              return redirect("login")  
            else:
                messages.error(request,"Some Problem occur in sending varification Password Change Sorry !! ")         
        else:
            messages.error(request,"Please Enter Invalid Email")
            return redirect("change")
    else:
        return render(request,"changepassword.html")                



# addcart

def addcart(request,id1):

    if 'is_loged' in request.session:
        userid=request.session.get('is_loged')
        userstr=str(userid)
        print(userstr)
        print(id1)
        try:
           if userstr in request.session:
              cartid=request.session.get(userstr)
              print(cartid)
              if id1 in cartid:
                messages.add_message(request,messages.ERROR,"Product is already in cart")
              else:
                cartid.append(id1)
                request.session[userstr]=cartid
                messages.add_message(request,messages.INFO,"Continew Shoping")
           else:
              request.session[userstr]=[id1]
              messages.add_message(request,messages.INFO,"Continew shoping")
        except:
            messages.error(request,"Something is worng")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
    else:
        return redirect('login')

#  end addcart
# start product discription

def proddesc(request,id2):
    # code for show description
    g=int(id2)
    print(g)
    p=product.objects.filter(id=g)
    # Code for converting description in dictionery
    temp=''
    for i in p:
        temp=i
    print(type(temp))
    print(temp)
    print(temp.desc)    
    descstr=''
    descstr=temp.desc
    descstr2=descstr.split(',')
    descstr3={k.split(':')[0]:k.split(':')[1]for k in descstr2} 
    # End Code of Dictionery
        # end----
    paymentlist=[]
    product_id=0   
    sum=0 
    # code provide username and cart size
    if request.session.has_key('is_loged'):
       userid=request.session.get('is_loged')
       username=request.session.get('is_name')
       userstr=str(userid)
       cartid=request.session.get(userstr)
       if cartid:
           n=len(cartid)
       else:
           n=0
       #start product desc table
       for i in p:
               if i.Available>0:
                   after=(i.price*(100-i.Offer))/100
                   sum=sum+after
                   abc={'name':i.product_name,'category':i.category,'color':i.color,'size':i.Size,'available':'Yes','offer':i.Offer,'price':i.price,'afterp':after}
               else:
                   abc={'name':i.product_name,'category':i.category,'color':i.color,'size':i.Size,'available':'No','offer':i.Offer,'price':i.price,'afterp':'Not consider'}
               paymentlist.append(abc) 
               product_id=i.id 

       request.session['pro_id2']=product_id   
        # End Code 
       params = {'login':'YES','lenth':n,'name':username,'product':p,'description':descstr3,'payment2':paymentlist,'Total':sum}
       return render(request,"Productdec.html",params)       
    else:
       n=0
       params = {'login':'','lenth':n,'product':p,'description':descstr3}
       return render(request,"Productdec.html",params)
# end_____--------
    return render(request,"Productdec.html")
# end product discription


def Bynow(request,id3):
    g=int(id3)
    productobj=product.objects.filter(pk=id3)
    temp=''
    for i in productobj:
        temp=i
    pavailable=temp.Available
    price=(temp.price*(100-temp.Offer))/100 
    if pavailable >0:
      orderid=0
    #   if userorder.objects.values('order_id'):
    #         porder1=userorder.objects.order_by('order_id')[0]
    #         orderid=porder1.order_id+1
    #   else:
    #         orderid=12350 
      if request.session.has_key('is_loged'):
         userid=request.session.get('is_loged')    
         useraddress=address.objects.filter(userid=userid)
         temp2=''
         for i in useraddress:
            temp2=i

         if temp2.countery:
            request.session['onepro_id']=g
            orderid=random.randint(123460,1234100)
            request.session['order_id1']=orderid
            print("Run this code")
            param_dict = {
            'MID': MID,
            'ORDER_ID': str(orderid),
            'TXN_AMOUNT': str(price),
            'CUST_ID': str(userid),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest1/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request, 'paytm.html', {'param_dict': param_dict})
             
         else:
            messages.error(request,"Please fill address for By")
            return redirect("dashbord")    
      else:
         messages.error(request,"Please login for By Now ")
         return render(request,"login.html")
    else:
        messages.error(request,"Product not available in stock")
        return redirect("about")
    return HttpResponse("....Sorry...")

# Handlerequest1 
@csrf_exempt
def handlerequest1(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            return redirect("oneorder") 
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})

# code for one order

def oneorder(request):
    tday=datetime.date.today()
    g=0
    orderid=0
    if request.session.get('onepro_id'):
        g=request.session['onepro_id']
        del request.session['onepro_id']
    else:
        messages.error(request,"Something is Worng")
        return redirect("about")
    if request.session.get('order_id1'):
        orderid=request.session['order_id1']
        del request.session['order_id1']
    else:
        messages.error(request,"Something is Worng")
        return redirect("about")    
    productobj=product.objects.filter(pk=g)
    temp=''
    for i in productobj:
        temp=i
    pavailable=temp.Available
    price=(temp.price*(100-temp.Offer))/100 
    pname=temp.product_name
    userid=request.session.get('is_loged')
    userobject=user.objects.filter(pk=userid)
    tempuobj=''
    for i in userobject:
        tempuobj=i
    Email=tempuobj.email    
    porder=userorder.objects.create(user_order=tempuobj,user_id=userid,product_id=g,product_name=pname,Track='Order Accept',price=price,order_date=tday,order_id=orderid)
    if porder:
        porder.save()
        pavailable=pavailable-1
        temp.sales=temp.sales+1
        temp.Available=pavailable
        temp.save()
        mail=send_mail("Inform for By now of Mycart","Your order successfull","ayadavupc@gmail.com",[Email],fail_silently=False,html_message='''<h3>Order is success on Email Id {} and Product Name is {} Order Date is {} For more information go on Dashbord </h3>'''.format(Email,pname,tday))
        if mail:
            messages.info(request,"Order Successfull continue shoping")
        else:
            messages.info(request,"Something is worng sending comform email")    
    else:
        messages.error(request,"something is worng") 
    return redirect("about") 
# end code-------------------------------------------------------------
            
def Zoom(request,id4):
    # code for username and cart size
    if request.session.has_key('is_loged'):
       userid=request.session.get('is_loged')
       username=request.session.get('is_name')
       userstr=str(userid)
       cartid=request.session.get(userstr)
       if cartid:
           n=len(cartid)
       else:
           n=0

       g=int(id4)
       print(g)
       p=product.objects.filter(id=g) 
       print(p)
       for i in p:
            print(i.product_name)
       params = {'login':'YES','lenth':n,'name':username,'product':p }
       return render(request,"zoom.html",params)      
    else:
       n=0
# ======================
       g=int(id4)
       print(g)
       p=product.objects.filter(id=g)
       for i in p:
           print(i.product_name)
        #    ==============
       params ={'login':'','lenth':n,'product':p }
       return render(request,"zoom.html",params)
# End
    
    

def search(request):
    # code provide username and cart size
    if request.session.has_key('is_loged'):
       userid=request.session.get('is_loged')
       username=request.session.get('is_name')
       userstr=str(userid)
       cartid=request.session.get(userstr)
       if cartid:
           n=len(cartid)
       else:
           n=0
       if  request.method=='POST':
           search=request.POST['search']
           print(search)
           if search:
               print(n)
               print(username)
               p=product.objects.filter(Q(product_name__icontains=search)|Q(category__icontains=search)|Q(subcategory__icontains=search)|
               Q(desc__icontains=search)|Q(Brand__icontains=search))
               if p:
                  print(n)
                  print(username)
                  params={'login':'YES','lenth':n,'name':username,'product':p}
                  return render(request,"search.html",params)
               else:
                  messages.error(request,"Not Record Found")
                  params={'login':'YES','lenth':n,'name':username}
                  return render(request,'search.html',params)
           else:
               messages.info(request,"Please search something")
               params={'login':'YES','lenth':n,'name':username}
               return render(request,"search.html",params)
       else:
           params={'login':'YES','lenth':n,'name':username}
           return render(request,"search.html",params)    
    else:
       n=0
       if  request.method=='POST':
           search=request.POST['search']
           print(search)
           if search:
               p=product.objects.filter(Q(product_name__icontains=search)|Q(category__icontains=search)|Q(subcategory__icontains=search)|
               Q(desc__icontains=search)|Q(Brand__icontains=search))
               if p:
                  params={'login':'','lenth':n,'product':p}
                  return render(request,"search.html",params)
               else:
                  messages.error(request,"Not Record Found")
                  params={'login':' ','lenth':n}
                  return render(request,'search.html',params)
           else:
               messages.info(request,"Please search something")
               params={'login':' ','lenth':n}
               return render(request,"search.html",params)
       else:
           params={'login':' ','lenth':n}
           return render(request,"search.html",params)         
# end_____--------



def filter(request):
    maxprice=product.objects.aggregate(Max('price'))
    minprice=product.objects.aggregate(Min('price'))
    maxprice=maxprice['price__max']
    maxprice=maxprice+100
    minprice=minprice['price__min']
    minprice=minprice-100
    allfilter=product.objects.values('Brand','category','color','Size','Quality').distinct()
    Brand={item['Brand'] for item in allfilter }
    category={item['category'] for item in allfilter }
    color={item['color'] for item in allfilter }
    Size={item['Size'] for item in allfilter }
    Quality={item['Quality'] for item in allfilter }
    # code for authentication
    if request.session.has_key('is_loged'):
        userid=request.session.get('is_loged')
        username=request.session.get('is_name')
        userstr=str(userid)
        cartid=request.session.get(userstr)
        if cartid:
           n=len(cartid)
        else:
           n=0
    #    ===========
        params={'brand':Brand,'Category':category,'Color':color,'size':Size,'quality':Quality,'minprice':minprice,'maxprice':maxprice,'login':'YES','lenth':n,'name':username}
        if request.method =='POST':
          Brand_request=request.POST['brand']
          quality_request=int(request.POST['quality'])
          Category_request=request.POST['category']
          Color_request=request.POST['color']
          Size_request=request.POST['size']
          Min_price_request=int(request.POST['minp'])
          Max_price_request=int(request.POST['maxp'])
          try:
             discount_request=int(request.POST['Discount'])
          except:
             messages.error(request,"Please set Discount")
             return render(request,"filter.html",params)    

          search_request=request.POST['search']
          if search_request:
            userfilter=product.objects.filter(Q(Brand__icontains=Brand_request)& Q(Quality=quality_request) & Q(category__icontains=Category_request)&
            Q(color__icontains=Color_request)& Q(Size__icontains=Size_request) & Q(price__gte=Min_price_request) & Q(price__lte=Max_price_request)  &
            Q(Offer__gte=discount_request) & Q(product_name__icontains=search_request))
            if userfilter:
                params={'brand':Brand,'Category':category,'Color':color,'size':Size,'quality':Quality,'product':userfilter,'minprice':minprice,'maxprice':maxprice,'login':'YES','lenth':n,'name':username}
                print(userfilter)
                return render(request,"filter.html",params)
            else:
                messages.error(request,"Not Record Found") 
                return render(request,"filter.html",params) 

          else:
              messages.error(request,"Please Search something")
              return render(request,"filter.html",params)  
        else:
            return render(request,"filter.html",params)             
    else:
        n=0
        # ============code for filter
        params={'brand':Brand,'Category':category,'Color':color,'size':Size,'quality':Quality,'minprice':minprice,'maxprice':maxprice,'login':'','lenth':n}
        if request.method =='POST':
          Brand_request=request.POST['brand']
          quality_request=int(request.POST['quality'])
          Category_request=request.POST['category']
          Color_request=request.POST['color']
          Size_request=request.POST['size']
          Min_price_request=int(request.POST['minp'])
          Max_price_request=int(request.POST['maxp'])
          try:
             discount_request=int(request.POST['Discount'])
          except:
             messages.error(request,"Please set Discount")
             return render(request,"filter.html",params)    

          search_request=request.POST['search']
          if search_request:
            userfilter=product.objects.filter(Q(Brand__icontains=Brand_request)& Q(Quality=quality_request) & Q(category__icontains=Category_request)&
            Q(color__icontains=Color_request)& Q(Size__icontains=Size_request) & Q(price__gte=Min_price_request) & Q(price__lte=Max_price_request)  &
            Q(Offer__gte=discount_request) & Q(product_name__icontains=search_request))
            if userfilter:
                params={'brand':Brand,'Category':category,'Color':color,'size':Size,'quality':Quality,'product':userfilter,'minprice':minprice,'maxprice':maxprice,'login':'','lenth':n}
                print(userfilter)
                return render(request,"filter.html",params)
            else:
                messages.error(request,"Not Record Found") 
                render(request,"filter.html",params) 

          else:
             messages.error(request,"Please Search something")
             return render(request,"filter.html",params) 

        else:
            return render(request,"filter.html",params)

    return render(request,"filter.html",params)


    # ===============


def showcart(request):
    if request.session.has_key('is_loged'):
       userid=request.session.get('is_loged')
       username=request.session.get('is_name')
       userstr=str(userid)
       cartid=request.session.get(userstr)
       if cartid:
           n=len(cartid)
           products=product.objects.filter(pk__in=cartid)
           productid=[]
           paymentlist=[]
           abc={}
           sum=0
           for i in products:
               if i.Available>0:
                   after=(i.price*(100-i.Offer))/100
                   sum+=after
                   productid.append(i.id)
                   abc={'name':i.product_name,'category':i.category,'color':i.color,'size':i.Size,'available':'Yes','offer':i.Offer,'price':i.price,'afterp':after}
               else:
                   abc={'name':i.product_name,'category':i.category,'color':i.color,'size':i.Size,'available':'No','offer':i.Offer,'price':i.price,'afterp':'Not consider'}
               paymentlist.append(abc)  
           request.session['pro_id']=productid 
           print(sum)   
           params = {'login':'YES','product': products,'lenth':n,'name':username,'payment':paymentlist,'Total':sum}
       else:
           n=0
           params = {'login':'YES','lenth':n,'name':username}
           messages.error(request,"Nothing Record Found !!") 
       return render(request,'showcart.html',params)         
    else:

        return redirect('login')

def deletecart(request,id4):
    userid=request.session.get('is_loged')
    userstr=str(userid)
    cartid=request.session.get(userstr)
    if id4 in cartid:
        cartid.remove(id4)
        request.session[userstr]=cartid
        messages.info(request,"Continue Shoping")
    else:
        messages.error(request,"No Match in cart !")   

    return redirect("showcart")

# dashbord-------
def dashbord(request):
    if request.session.has_key('is_loged'):
       userid=request.session.get('is_loged')
       username=request.session.get('is_name')
       userstr=str(userid)
       cartid=request.session.get(userstr)
       if cartid:
           n=len(cartid)
       else:
           n=0
       user_details=user.objects.filter(pk=userid)
       print(user_details)
       user_address=address.objects.filter(userid=userid)
       user_order=userorder.objects.filter(user_id=userid) 
       allstate=state.objects.all()    
       params = {'login':'YES','lenth':n,'name':username,'userdetails':user_details,'useraddress':user_address,'userorder':user_order,'allstate':allstate}
       return render(request,"user_dashbord.html",params)
    else:
        return redirect("login")    
    return HttpResponse("please fill address") 

 # delete order
def deleteorder(request,id5):
    tday=datetime.date.today()
    usero=userorder.objects.filter(pk=id5)
    temp1=''
    for i in usero:
        temp1=i
    productid=temp1.product_id
    delete_order=orderdelete.objects.create(productname=temp1.product_name,userid=temp1.user_id,productid=temp1.product_id,orderdate=temp1.order_date,deletedate=tday,Track=temp1.Track,order_id=temp1.order_id)
    delete_order.save()
    usero.delete()
    productobj=product.objects.filter(pk=productid)
    temp2=''
    for i in productobj:
        temp2=i
    available=temp2.Available
    temp2.Available=available+1
    temp2.sales=temp2.sales-1
    temp2.save()    
    messages.info(request,"Cancle order Successfull")
    return redirect("dashbord")

# reating Code
def reating(request):
    userid=request.session.get('is_loged')
    if request.method == 'POST':
        productid=request.POST['productid']
        reating=request.POST['rate']
        userid=request.session.get('is_loged')
        intreating=int(reating)
        print(productid,reating,userid,intreating)
        userorderobj=userorder.objects.filter(user_id=userid)
        temp=''
        for i in userorderobj:
            temp=i
        rate=product_rating.objects.create(userrate=temp,userid_rating=userid,productid_rating=productid,rating=intreating)
        if rate:
           rate.save()
           print("Yess")
           messages.info(request,"Thanks For Reating Product")
        else:
            print("No")
            messages.error(request,"Something is Worng")   
        return redirect("dashbord")
    else:
        return render(request,"index.html")    


# Change account 
def chageaccount(request):
    if request.method == 'POST':
        username=request.POST['username']
        useremail=request.POST['useremail']
        if user.objects.filter(email=useremail).exists():
            messages.error(request,"User is alredy exists plaese choose another email")
            return redirect("dashbord")
        else:
            userid=request.session.get('is_loged')
            userobj=user.objects.filter(pk=userid)
            temp=''
            for i in userobj:
                temp=i

            temp.name=username
            temp.email=useremail
            temp.save()
            mail=send_mail("Account Details Change of Mycart","Your Details Change Successfully","ayadavupc@gmail.com",[useremail],fail_silently=False,html_message='''<h3>We Inform that your account details is change new email {} and New Phone no is {} aney Query Please Contect me {}</h3>'''.format(useremail,8318167080))
            if mail:
                messages.info(request,"Your Account  Successfully Change")
                return redirect("dashbord")  
            else:
                messages.error(request,"Some Problem occur in sending varification Password Change Sorry !! ")         
    else:
        return render(request,"user_dashbord")

# Feedback code
def Feedback(request):
    if request.method == 'POST':
        useremail=request.POST['useremail']
        userfeedback=request.POST['userfeedback']
        recaptcha_response = request.POST.get('g-recaptcha-response')
        print(useremail)
        data = {
                'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()    
        if result['success']:
            obj=feedback()
            if obj:
                obj.user_email=useremail
                obj.user_feedback=userfeedback
                obj.save()
                messages.info(request,"Thanks for gaving Feedback")
            else:
                messages.error(request,"Something is worng")    
        else:
            messages.error(request,'Invalid Captcha!')
        return redirect("about")
    else:
        return redirect("about")                

 # addaddress
def addaddress(request):
    if request.method == 'POST':
        usercountery=request.POST['countery']
        userstate=request.POST['state']
        userdistrict=request.POST['district'] 
        userpost=request.POST['pots']
        uservillage=request.POST['village']
        userhomeno=request.POST['home']
        checkme=request.POST['check']
        phone=request.POST['phone']
        print(usercountery,userdistrict,userstate,uservillage,userhomeno,checkme)
        if "Choose" in userstate:
            messages.error(request,"Please Choose State")
            return redirect("dashbord")
        else:
            userid=request.session.get("is_loged")
            userobj=user.objects.filter(pk=userid)
            temp=''
            useraddobj=address.objects.filter(userid=userid) 
            for i in useraddobj:
                temp =i
            if useraddobj:
                temp.countery=usercountery
                temp.state=userstate
                temp.district=userdistrict
                temp.post=userpost
                temp.village=uservillage
                temp.Home_No=userhomeno  
                temp.phone=phone  
                temp.save()
                messages.info(request,"Your Address is Successfull add  ")
                return redirect("dashbord")
            else:
                messages.error(request,"Something is worng")
                return redirect("dashbord")

    else:
        return redirect("dashbord")    

# Change address

def changeaddress(request):
    if request.method == 'POST':
        usercountery=request.POST['countery']
        userstate=request.POST['state']
        userdistrict=request.POST['district'] 
        userpost=request.POST['pots']
        uservillage=request.POST['village']
        userhomeno=request.POST['home']
        checkme=request.POST['check']
        phone=request.POST['phone']
        print(usercountery,userdistrict,userstate,uservillage,userhomeno,checkme)
        if "Choose" in userstate:
            messages.error(request,"Please Choose State")
            return redirect("dashbord")
        else:
            userid=request.session.get("is_loged")
            userobj=user.objects.filter(pk=userid)
            temp=''
            useraddobj=address.objects.filter(userid=userid) 
            for i in useraddobj:
                temp =i
            if useraddobj:
                temp.countery=usercountery
                temp.state=userstate
                temp.district=userdistrict
                temp.post=userpost
                temp.village=uservillage
                temp.Home_No=userhomeno 
                temp.phone=phone
                temp.save()
                messages.info(request,"Your Address is Successfull change  ")
                return redirect("dashbord")
            else:
                messages.error(request,"Something is worng")
                return redirect("dashbord")

    else:
        return redirect("dashbord")    

def multiorder(request):
    if request.method=='POST':
        if request.session.has_key('is_loged'):
            request.session['checkmul']='check'
            userid=request.session.get('is_loged')
            print(userid)
            useraddress=address.objects.filter(userid=userid)
            temp2=''
            for i in useraddress:
                temp2=i
            if temp2.countery:

                userobject=user.objects.filter(pk=userid)
                tempuobj=''
                for i in userobject:
                    tempuobj=i

                Email=tempuobj.email 
                orderid=0
                # if userorder.objects.values('order_id'):
                #     porder1=userorder.objects.order_by('order_id')[0]
                #     orderid=porder1.order_id+1
                # else:
                #     orderid=123450
                orderid=random.randint(123460,1234100)
                sum=0   
                if 'pro_id' in request.session:
                    productid=request.session.get('pro_id')
                    if productid:
                        productobj=product.objects.filter(pk__in=productid)
                        for i in productobj:

                            price=(i.price*(100-i.Offer))/100 
                            sum=sum+price   
                        print("Run this code")
                        orderid=random.randint(123460,1234100)
                        request.session['order_id2']=orderid
                        param_dict = {
                        'MID': MID,
                        'ORDER_ID': str(orderid),
                        'TXN_AMOUNT': str(sum),
                        'CUST_ID': str(userid),
                        'INDUSTRY_TYPE_ID': 'Retail',
                        'WEBSITE': 'WEBSTAGING',
                        'CHANNEL_ID': 'WEB',
                        'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest2/',
                        }
                        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
                        return render(request, 'paytm.html', {'param_dict': param_dict})
                    else:
                        messages.error(request,"Product is not Avilable in stock") 
                        return redirect("showcart")    
            else:
                messages.error(request,"Please fill address for By")
                return redirect("dashbord")
        else:
            messages.error(request,"Please login for By Now ")
            return render(request,"login.html")
    else:
            return redirect("showcart")
    return HttpResponse("....Sorry...")
#
# End Code
#     
@csrf_exempt
def handlerequest2(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    print(response_dict)
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            return redirect("multiordercreate")    
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})        
    
# Multioredercreate
def multiordercreate(request):
    if 'pro_id' in request.session:
            productid=request.session.get('pro_id')
            del request.session['pro_id']
            orderid=request.session.get('order_id2')
            del request.session['order_id2']
            if 'checkmul' in request.session:
                del request.session['checkmul']
                tday=datetime.date.today()
                allpname=[]
                userid=request.session.get('is_loged')
                userobject=user.objects.filter(pk=userid)
                userid=request.session.get('is_loged')
                tempuobj=''
                for i in userobject:
                    tempuobj=i

                Email=tempuobj.email
                # if userorder.objects.values('order_id'):
                #     porder1=userorder.objects.order_by('order_id')[0]
                #     orderid=porder1.order_id+1
                # else:
                #     orderid=12350
                productobj=product.objects.filter(pk__in=productid)
                for i in productobj:
                    g=i.id
                    price=(i.price*(100-i.Offer))/100
                    pname=i.product_name
                    allpname.append(pname)
                    porder=userorder.objects.create(user_order=tempuobj,user_id=userid,product_id=g,product_name=pname,Track='Order Accept',price=price,order_date=tday,order_id=orderid)
                    pavailable=i.Available
                    pavailable=pavailable-1
                    i.sales=i.sales+1
                    i.Available=pavailable
                    i.save()
                if porder:
                    porder.save()
                    mail=send_mail("Inform for By now of Mycart","Your order successfull","ayadavupc@gmail.com",[Email],fail_silently=False,html_message='''<h3>Order is success on Email Id {} and Product Name is {} Order Date is {} Order Id {} For more information go on Dashbord </h3>'''.format(Email,allpname,tday,orderid))
                    if mail:
                         messages.info(request,"Order Successfull continue shoping")
                    else:
                        messages.error(request,"Something is worng sending comform email")
                else:
                    messages.error(request,"Order is not create")        
            else:
                messages.error(request,"Something is worngabc")
    else:
        messages.error(request,"Something is Worng")

    return redirect("about")




# start code for more discount
def morediscount(request):
    if request.session.has_key('is_loged'):
       userid=request.session.get('is_loged')
       username=request.session.get('is_name')
       userstr=str(userid)
       cartid=request.session.get(userstr)
       if cartid:
           n=len(cartid)
       else:
           n=0
       
       p=product.objects.filter(Q(Offer__gte=75))
       if p:
            print(n)
            print(username)
            params={'login':'YES','lenth':n,'name':username,'product':p}
            return render(request,"search.html",params)
       else:
            messages.error(request,"Not Record Found")
            params={'login':'YES','lenth':n,'name':username}
            return render(request,'search.html',params)   
    else:
      
       n=0

       p=product.objects.filter(Q(Offer__gte=75))
       if p:
            print(n)
            print(username)
            params={'login':'YES','lenth':n,'name':username,'product':p}
            return render(request,"search.html",params)
       else:
            messages.error(request,"Not Record Found")
            params={'login':'YES','lenth':n,'name':username}
            return render(request,'search.html',params)       
    
# Code for premium
def premimum(request):
    if request.session.has_key('is_loged'):
       userid=request.session.get('is_loged')
       username=request.session.get('is_name')
       userstr=str(userid)
       cartid=request.session.get(userstr)
       if cartid:
           n=len(cartid)
       else:
           n=0
       
       p=product.objects.filter(Premimum=True)
       if p:
            print(n)
            print(username)
            params={'login':'YES','lenth':n,'name':username,'product':p}
            return render(request,"search.html",params)
       else:
            messages.error(request,"Not Record Found")
            params={'login':'YES','lenth':n,'name':username}
            return render(request,'search.html',params)   
    else:
       n=0
       p=product.objects.filter(Premimum=True)
       if p:
            print(n)
            print(username)
            params={'login':'YES','lenth':n,'name':username,'product':p}
            return render(request,"search.html",params)
       else:
            messages.error(request,"Not Record Found")
            params={'login':'YES','lenth':n,'name':username}
            return render(request,'search.html',params)       
    
# Code for More selling
def moreselling(request):
    if request.session.has_key('is_loged'):
       userid=request.session.get('is_loged')
       username=request.session.get('is_name')
       userstr=str(userid)
       cartid=request.session.get(userstr)
       if cartid:
           n=len(cartid)
       else:
           n=0
       
       p=product.objects.filter(Q(sales__gt=5))
       if p:
            print(n)
            print(username)
            params={'login':'YES','lenth':n,'name':username,'product':p}
            return render(request,"search.html",params)
       else:
            messages.error(request,"Not Record Found")
            params={'login':'YES','lenth':n,'name':username}
            return render(request,'search.html',params)   
    else:
       
       n=0

       p=product.objects.filter(Premimum=True)
       if p:
            print(n)
            print(username)
            params={'login':'YES','lenth':n,'name':username,'product':p}
            return render(request,"search.html",params)
       else:
            messages.error(request,"Not Record Found")
            params={'login':'YES','lenth':n,'name':username}
            return render(request,'search.html',params)
            
# Payment Example
def payment(request):
    print("Run this code")
    param_dict = {

                'MID': MID,
                'ORDER_ID': str(1256),
                'TXN_AMOUNT': str(15),
                'CUST_ID':'457',
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'paytm.html', {'param_dict': param_dict})



# Pdf code-------------------------------------

# pip install --pre xhtml2pdf 
# ----------------------------------------------------------
def pdfdownload(request):
    if request.method=='POST':
        orderid=request.POST['orderid']
        orderid=int(orderid)
        print(orderid)
        tday=datetime.date.today()
        orderobj=userorder.objects.filter(order_id=orderid) 
        if orderobj:
            temp1=0
            for i in orderobj:
                temp1=i
            userobj=user.objects.filter(pk=temp1.user_id) 
            addressobj=address.objects.filter(userid=temp1.user_id)
            print(addressobj)
            sum=0
            for i in orderobj:
                sum=sum+i.price      

            data={'orderobj':orderobj,'userobj':userobj,'sum':sum,'Date':tday,'address':addressobj}    
            pdf = render_to_pdf('orderpdf.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            messages.error(request,"Order is not exists") 
            return render(request,'pdfdownload.html')   
        
    else:
        return render(request,'pdfdownload.html')    



