from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from social_django.models import UserSocialAuth

# Create your models here.
class user(models.Model):
    name=models.CharField(max_length=50,help_text='User name')
    email=models.CharField(max_length=60)
    password=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class product(models.Model):
    color_name=[('none','none'),('Red','Red'),('Blue','Blue'),('Green','Green'),('Orange','Orange'),('Yellow','Yellow'),('Pink','Pink'),('Purple','Purple'),('Violet','Violet'),('Gold','Gold'),('Coral','Coral'),('Brown','Brown'),('White','white'),('Black','Black'),('Silver','Silver')]
    c_size=[('none','none'),('S size','S size'),('M size','M size'),('L size','L size')]
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50,default='')
    subcategory=models.CharField(max_length=50, default='')
    price=models.IntegerField(default=0)
    desc=models.TextField(max_length=300,help_text='Please Enter is format color : Red , ......just like  ')
    Offer=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)])
    Available=models.IntegerField(default=0)
    Premimum=models.BooleanField(default=False)
    Feature=models.BooleanField(default=False)
    Brand=models.CharField(max_length=50)
    color=models.CharField(max_length=15,choices=color_name,default='none')
    Size=models.CharField(max_length=10,choices=c_size,default='none')
    Quality=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(4)])
    p_rate=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(4)])
    pub_date=models.DateTimeField(auto_now=False)
    sales=models.IntegerField(default=0)
    Image1=models.ImageField(upload_to="shop/image",default='')
    Image2=models.ImageField(upload_to="shop/image",default='')
    Image3=models.ImageField(upload_to="shop/image",default='')

    def __str__(self):
        return self.product_name

# Moodel for user address
class address(models.Model):
    userconnection=models.OneToOneField(to=user,on_delete=CASCADE, default='')
    userid=models.IntegerField(default=0)
    countery=models.CharField(max_length=30 ,default='')
    state=models.CharField(max_length=30,default='')
    district=models.CharField(max_length=30,default='')
    post=models.CharField(max_length=30,default='')
    village=models.CharField(max_length=30,default='')
    Home_No=models.CharField(max_length=50,default='')
    phone=models.CharField(max_length=10)
   

#  model for order

class userorder(models.Model):
    user_order=models.ForeignKey(to=user,on_delete=CASCADE)
    user_id=models.IntegerField(default=0)
    product_id=models.IntegerField(default=0)
    product_name=models.CharField(max_length=30,default='')
    order_date=models.DateField(auto_now=True)
    Track=models.CharField(max_length=30,default='')
    price=models.IntegerField(default=0)
    order_id=models.IntegerField(default=0)
    # product_rate=models.IntegerField(default=0)
    delevered_date=models.DateField(blank=True,auto_now=False,null=True)

    def __str__(self):
        return self.Track

class product_rating(models.Model):
    userrate=models.ForeignKey(to=userorder,on_delete=CASCADE)
    userid_rating=models.IntegerField(default=0)
    productid_rating=models.IntegerField(default=0)
    rating=models.IntegerField(default=0)

    def __str__(self):
        return self.userid_rating

 # End
 # Code for Counter Model
class countery(models.Model):
    countery_name=models.CharField(max_length=40,default='')
    def __str__(self):
        return self.countery_name

 # Code for Sates

class state(models.Model):
    In_countery=models.ForeignKey(to=countery,on_delete=CASCADE)
    state_name=models.CharField(max_length=40,default='')
    def __str__(self):
        return self.state_name

# Code for District
class District(models.Model):
    In_state=models.ForeignKey(to=state,on_delete=CASCADE)
    District_name=models.CharField(max_length=40,default='') 
    Ofstate=models.CharField(max_length=40,default='')
    def __str__(self):
        return self.District_name


# Feedback Model
class feedback(models.Model):
    user_email=models.CharField(max_length=40,default='')
    user_feedback=models.TextField(max_length=300,default='')
    
# Order delete Model
class orderdelete(models.Model):
    productname=models.CharField(max_length=100,default='')
    userid=models.IntegerField(default=0)
    productid=models.IntegerField(default=0)
    order_id=models.IntegerField(default=0)
    orderdate=models.DateField()
    Track=models.CharField(max_length=40,default='')
    deletedate=models.DateField(auto_now=False)

    def __str__(self):
        return self.productname


# signal for address
def create_address(sender, **Kwargs):
    if Kwargs['created']:
        user_address=address.objects.create(userconnection=Kwargs['instance'],userid=(Kwargs['instance']).id)
        print(Kwargs['instance'])
        print((Kwargs['instance']).id)

post_save.connect(create_address,sender=user)   

# signal for changing rat of product in product model
def change_rate(sender, **Kwargs):
    if Kwargs['created']:
        productid=(Kwargs['instance']).productid_rating
        userrate=(Kwargs['instance']).rating
        productobj=product.objects.filter(pk=productid)
        temp=''
        for i in productobj:
            temp=i
        oldrat=temp.p_rate
        if oldrat < userrate:
            temp.p_rate=userrate
            temp.save()
        else:
            pass
        print((Kwargs['instance']).id)
    else:
        pass

post_save.connect(change_rate,sender=product_rating)  
# End Code  
# signal for changing sale of product
def change_sale(sender, **Kwargs):
    if Kwargs['created']:
        productid=(Kwargs['instance']).product_id
        productobj=product.objects.filter(pk=productid)
        temp=''
        for i in productobj:
            temp=i
        oldsale=temp.sales
        oldsale=oldsale+1
        temp.sales=oldsale
        temp.save()
    else:
        print("no")
post_save.connect(change_sale,sender=userorder)
# end code

# signal for spocial app
def create_user(sender, **Kwargs):
    if Kwargs['created']:
        u=user.objects.create(name=(Kwargs['instance'].user).username,email=(Kwargs['instance']).uid)
        print(Kwargs['instance'])
        print((Kwargs['instance']).id)

post_save.connect(create_user,sender=UserSocialAuth)

        