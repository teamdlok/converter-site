import uuid

from django.db import models
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """"
    Название категории, например, "Компьютеры", или "Инструменты" или "Автотовары"
    """
    name = models.CharField(
        verbose_name=_("Category name"),
        help_text=_("Unique"),
        max_length=255,
        unique=True
    )
    # Название категории, например, "Компьютеры", или "Инструменты" или "Автотовары"
    slug = models.SlugField(
        verbose_name=_("Product category unique URL"),
        max_length=255,
        unique=True
    )
    # Слаг для категории товара
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse('by_category_url', kwargs={'by_category': self.slug})

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    Тип продукта, например, в категории "Компьютеры" будут типы продуктов: "Компьютеры, Ноутбуки",
    "Комплектующие для пк", "Переферия".

     Для категории "Инструменты" будут типы продуктов: "Аккумуляторные инструменты", "Электроинструменты",
     "Ручные инструменты", "Техника для сада".

     Для категории "Автотовары" будут типы продуктов: "Автоэлектроника",
    "Автозвук", "Кресла", "Автосвет".
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Ключ
    name = models.CharField(verbose_name=_("Product type name"),
                            help_text=_("Required, unique"),
                            max_length=255,
                            unique=True)
    slug = models.SlugField(
        verbose_name=_("Product type unique URL"),
        max_length=255,
        unique=True
    )
    # Слаг для типа

    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('by_producttype_url', kwargs={'by_category': self.category.slug,
                                                     'by_producttype': self.slug})

    def __str__(self):
        return self.name


class ProductSubType(models.Model):
    """"
    Подтип продукта, например, в типе продукта "Компьютеры, ноутбуки" будут подтипы: "Персональне компьютеры",
    "Ноутбуки", "Моноблоки", "Тонкие клиенты", "Платформы", "Платформцы для моноблоков".

    В типе продукта "Аккумуляторные инструменты" будут подтипы: "Аккумуляторные платформы", "Аккумуляторные зарядные
    устройства", "Инструменты для сверления".

    В типе продукта "Автоэлектроника" будут подтипы: "Автомобильные ЗУ", "Видеорегистраторы", "Радар-детекторы",
    "Пуско-зарядные устройства", "Противоугонные системы и безопасность".
    """

    producttype = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    # Ключ
    name = models.CharField(verbose_name=_("Subtype name"),
                            help_text=_("Required, unique"),
                            max_length=255,
                            unique=True)
    slug = models.SlugField(
        verbose_name=_("Product sub type unique URL"),
        max_length=255,
        unique=True
    )

    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('url_by_productsubtype', kwargs={'by_category': self.producttype.category.slug,
                                                        'by_producttype': self.producttype.slug,
                                                        'by_productsubtype': self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Тут мы создаём объект продукта, который исходит от подтипа.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    productsubtype = models.ForeignKey(ProductSubType, on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_("Product"),
                            help_text=_("Product for store"),
                            max_length=255, )
    slug = models.SlugField(
        verbose_name="Product unique URL",
        max_length=255,
        unique=True, )

    regular_price = models.DecimalField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 99999.99"),
        error_messages={
            "name": {
                "max_lenght": _("The price must be between 0 and 99999.99")
            },
        },
        max_digits=7,
        decimal_places=2,
    ),

    discount_price = models.DecimalField(
        verbose_name=_("Discount price"),
        help_text=_("Maximum 99999.99"),
        error_messages={
            "name": {
                "max_lenght": _("The price must be between 0 and 99999.99")
            },
        },
        max_digits=7,
        decimal_places=2,
    ),

    is_active = models.BooleanField(default=True,
                                    verbose_name=_("Product visibility"),
                                    help_text=_("Change product visibility"), )

    created_at = models.DateTimeField(verbose_name=_("Created at"),
                                      auto_now_add=True,
                                      editable=False, )

    update_at = models.DateTimeField(verbose_name=_("Update at"),
                                     auto_now_add=True,
                                     editable=True, )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        return reverse('store_store:product_detail_url', kwargs={'id': self.id,})

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    """
            Тут мы делаем хранилище для картинок нашего товара. У одного товара может быть много картинок
            """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Ключ
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload product image"),
        upload_to="product-images/",
        default="product-images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative text for image"),
        help_text=_("Please add alternative text"),
        max_length=255,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")


class ProductSubTypeSpecification(models.Model):
            """
            Характеристики для подтипа товаров (Например, для "Персональне компьютеры",
            "Ноутбуки", "Моноблоки", "Тонкие клиенты", "Платформы", "Платформцы для моноблоков.

            Связан с ProductSubType ключом
            """

            productsubtype = models.ForeignKey(ProductSubType, on_delete=models.CASCADE)
            name = models.CharField(verbose_name=_("Name"),
                                    help_text="Required",
                                    max_length=255,
                                    )

            class Meta:
                verbose_name = _("Specification for product")
                verbose_name_plural = _("specifications for product")

            def __str__(self):
                return self.name


class ProductSpecificationFields(models.Model):
    """
    Заполняемые поля характеристик для товара

    Связан с Product ключом
    """

    productspecification = models.ForeignKey(ProductSubTypeSpecification, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    value = models.CharField(
        verbose_name=_("Value"),
        help_text=_("Product specification value (255 words)"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product cpecification value")
        verbose_name_plural = _("Product cpecification values")

    def __str__(self):
        return self.value