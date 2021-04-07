# Onlineshop
# Information
I am create this e commerce websit with django web framwork. This app provide functionality of e commerce related service like selling product. dispaly product on screen. payment of money etc.
User visit first page that dispaly like more selling product, feature poduct, more descount product. It us also provide user feedback with googe r-captcha. funtionality of this product:-

 * **login :** User login with email id or password or also google account.
 * **New account:** User have no account then he create account.

 * **Search product:** User search product with name or other like description info.
 * **Filter product:** User filter product with name, price, color, size,brand etc.
 * **Product Information:** User show all information of product.
 * **Add cart/remove:** User add/remove product in cart.
 * **Zoom product:** User show product with zoom.
 * **Dashbord:** User dashbord show user order, address info, account info, or provide to change acount info or delete order.

 * **Payment:** user payment with paytem gatway.
 * **Admin login:** Admin login this page this page provide django default.

 * **Admin Dashbord:** Admin add product, delete product, show order, cancele order,print order, add address, he perfom all functionality that are provide default by django. 

# Screenshot
![](Ecommerce/mycart/mycart/static/image/shop.png
)
# Files/foder in onlineshop app

  * **Settings:** This is the main file of django app. This is contain configuration system like all install app , database, middleware,templates etc.
  * **models:** This is contain blueprint of all database table in python class.This si user, product, address, userorder, product_reating, Feedback, orderdelete or signals  
  * **urls:** This is contain urls. In this project two urls file root urls or in side shop app urls. Ecah url map with specefic method.
  * **views:** This is contain action of method that are contain urls file.
  * **admin:** Django provide default admin page so it is required to register this models inside admin file or also provide features to filter,search, show coloum ect.
  * __init__: It is describe it is a python package.
  * **Pycache:** This is contain byte code after complitation of python code.
  * **migration folder:** This is contain blueprint of table in code formate after migrate command it is apply on actual database table.

  * **template:** This is contain html page like userlogin, dashbord, payment, odderpdf, filter, index, search, showcart, newaccount, varification, zoom etc.
  * **manage:** Django's command-line utility for administrative tasks. runserver, makemigration, migrate, createsuperuser etc.      

# Features of onlineshop
  * Newaccount creatation with email varification.
  * This is dynamic website.
  * Payment option.
  * make a pdf of user order.
  * effactive admin portal.
  * provide cart facility.
  * Feedback system.

# Deploy  
I use heroku free host website paltform for testing purpose. I use postgress object oriented database system.
  * downlaod heroku CLI
  * add import django_heroku in setting file.
  * DEBUG =False.
  * ALLOWED_HOSTS = ["app url"]

I use some command:-
 ```
 myenv\scripts\activate.bat
 pip install gunicorn
 pip freeze > requirement.txt
 git init
 git add .
 git commit -m '-------'
 heroku login
 git:remote -a 'name of heroku app'
 git push heroku master
 heroku run bash
 python manage.py makemigrations
 python manage.py migrate
 python manage.py runserver 
 ```

 # Run Chatapp
 My onlinecartshop is host on heroku server. you can visit click on this link :
 [onlineshop](https://onlinecityshop.herokuapp.com/shop)
