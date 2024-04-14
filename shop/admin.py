from django.contrib import admin

from shop import models


# Register your models here.
class ItemsPhotoInline(admin.StackedInline):
    model = models.ItemsPhoto
    extra = 0
    min_num = None
    max_num = None


class ItemInline(admin.TabularInline):
    model = models.Item
    readonly_fields = ("final_price",)
    extra = 0
    min_num = None
    max_num = None


@admin.register(models.ItemInfo)
class ItemInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "summary", "price", "title_photo")
    inlines = (ItemsPhotoInline,)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "is_payed", "get_current_total_price", "get_total_items")
    inlines = (ItemInline,)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("username",)
