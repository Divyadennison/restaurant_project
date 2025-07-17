from django.contrib import admin
from .models import Category, MenuItem, Reservation,Order, OrderItem,Review  

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Reservation)  
admin.site.register(OrderItem)
admin.site.register(Order)

admin.site.register(Review)
