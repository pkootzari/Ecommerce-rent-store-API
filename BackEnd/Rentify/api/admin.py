from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.WeekDay)
admin.site.register(models.Company)
admin.site.register(models.CompanyImage)
admin.site.register(models.CompanySubscription)
admin.site.register(models.Customer)
admin.site.register(models.ContactInfo)
admin.site.register(models.PhoneNumber)
admin.site.register(models.Address)
admin.site.register(models.Invoice)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.Tag)
admin.site.register(models.Rating)
admin.site.register(models.Basket)
admin.site.register(models.Item)
admin.site.register(models.Order)
admin.site.register(models.Fee)
