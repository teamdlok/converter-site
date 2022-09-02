from django.contrib import admin

from .models import *
# Register your models here.

from django import forms
from django.contrib import admin

from .models import (
    Category,
    Product,
    ProductImage,
    ProductSubTypeSpecification,
    ProductSpecificationFields,
    ProductType,
)


class CategoryInline(admin.TabularInline):
    model = Category


class ProductTypeInline(admin.TabularInline):
    model = ProductType


class ProductSubTypeInline(admin.TabularInline):
    model = ProductSubType


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSubTypeSpecification


@admin.register(Category)
class ProductTypeInline(admin.ModelAdmin):
    inlines = [
       ProductTypeInline,
    ]


@admin.register(ProductType)
class ProductTypeInline(admin.ModelAdmin):
    inlines = [
        ProductSubTypeInline,
    ]


@admin.register(ProductSubType)
class ProductTypeSpecificationsInline(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]


@admin.register(ProductImage)
class ProductImages(admin.ModelAdmin):
    inlines = []


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationFieldsInline(admin.TabularInline):
    model = ProductSpecificationFields


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        ProductSpecificationFieldsInline,
    ]

