from django.contrib import admin
from .models import user
from .models import product,address,userorder,product_rating,countery,state,District,feedback,orderdelete
from django.contrib.admin.options import ModelAdmin
# Register your models here.
class exampleuser(ModelAdmin):
    list_display=["name","email"]
    search_fields=["name","id"]
    list_filter=["id"]

class examproduct(ModelAdmin):
    list_display=["product_name","category","price","pub_date"]
    search_fields=["product_name","id"]
    list_filter=["pub_date","category","price"]

#admin.site.register(user)
class sadmin_address(ModelAdmin):
    list_display=["userid","countery","Home_No"]
    search_fields=["userid","countery","state","district","Home_No"]
    list_filter=["countery","state","district","village"]

# -----------------------
class sadmin_order(ModelAdmin):
    list_display=["order_id","user_id","product_id","product_name","order_date","Track","delevered_date"]
    search_fields=["userid_id","product_id","product_name"]
    list_filter=["order_date","Track","delevered_date","product_id"]
# -------------------------------------------
class sadmin_rating(ModelAdmin):
    list_display=["userrate","userid_rating","productid_rating","rating"]
    search_fields=["rating","userid_rating"]
    list_filter=["rating","productid_rating"]    
#----------------------------------------------- 
class delete_order(ModelAdmin):
    list_display=["productname","order_id","orderdate","deletedate","Track"]
    search_fields=["order_id","userid"]
    list_filter=["deletedate"]
#------------------------------------------------------------
admin.site.register(feedback)    
admin.site.register(countery)
admin.site.register(state)
admin.site.register(District)
admin.site.register(user,exampleuser)
admin.site.register(product,examproduct)
admin.site.register(address,sadmin_address)
admin.site.register(userorder,sadmin_order)
admin.site.register(product_rating,sadmin_rating)
admin.site.register(orderdelete,delete_order) 