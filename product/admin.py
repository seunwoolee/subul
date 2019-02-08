from django.contrib import admin
from django.db import models

from django_select2.forms import Select2Widget
from .models import Product, ProductAdmin, ProductCode, ProductMaster, ProductEgg, ProductUnitPrice, SetProductCode \
    , SetProductMatch


class ProductsAdmin(admin.ModelAdmin):
    list_filter = ["id"]
    list_display = ["id", "ymd", "codeName", 'type']
    search_fields = ["id", "ymd", "codeName"]


class ProductsCodeAdmin(admin.ModelAdmin):
    list_filter = ["code"]
    list_display = ["code", "codeName", "delete_state", "type", "amount_kg"]
    search_fields = ["code", "codeName"]


class ProductAdminAdmin(admin.ModelAdmin):
    raw_id_fields = ["product_id"]
    list_filter = ["id"]
    list_display = ["product_id", "ymd", "releaseType", "releaseSeq", "location"]
    exclude = ["releaseSeq", "product_id"]


class ProductMasterAdmin(admin.ModelAdmin):
    list_filter = ["ymd"]
    list_display = ["ymd", "total_loss_openEgg", "total_loss_insert", "total_loss_clean",
                    "total_loss_fill"]
    search_fields = ["ymd"]

    def get_queryset(self, request):
        queryset = super(ProductMasterAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-ymd')
        return queryset


class ProductEggAdmin(admin.ModelAdmin):
    list_filter = ["ymd"]
    list_display = ["ymd", "codeName", "type"]
    search_fields = ["ymd", "codeName"]

    def get_queryset(self, request):
        queryset = super(ProductEggAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-ymd')
        return queryset


class ProductUnitPriceAdmin(admin.ModelAdmin):
    list_display = ["locationCode", "productCode", "price", "specialPrice", "delete_state"]
    search_fields = ["locationCode__codeName", "productCode__codeName"]
    formfield_overrides = {
        models.ForeignKey: {'widget': Select2Widget}
    }

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
            '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.5/js/select2.min.js',
        )


class SetProductCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "codeName", "location", "delete_state"]
    search_fields = ["location__codeName", "codeName"]
    formfield_overrides = {
        models.ForeignKey: {'widget': Select2Widget}
    }

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
            '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.5/js/select2.min.js',
        )


class SetProductMatchAdmin(admin.ModelAdmin):
    list_display = ["setProductCode", "productCode", "saleLocation", "price", "delete_state"]
    search_fields = ["setProductCode__codeName", "saleLocation__codeName"]
    formfield_overrides = {
        models.ForeignKey: {'widget': Select2Widget}
    }

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
            '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.5/js/select2.min.js',
        )


admin.site.register(Product, ProductsAdmin)
admin.site.register(ProductCode, ProductsCodeAdmin)
admin.site.register(ProductAdmin, ProductAdminAdmin)
admin.site.register(ProductMaster, ProductMasterAdmin)
admin.site.register(ProductEgg, ProductEggAdmin)
admin.site.register(ProductUnitPrice, ProductUnitPriceAdmin)
admin.site.register(SetProductCode, SetProductCodeAdmin)
admin.site.register(SetProductMatch, SetProductMatchAdmin)

