from django.core.management.base import BaseCommand, CommandError
from core.models import Category, ProductColor, ProductSize, Product, ProductGroup, ProductSKU
from core.data.category import roots_category, clothes_category
from core.data.product import colors_list, sizes_list, products_list, groups_list, product_sku_list

def insert_category():
    for item in roots_category:
        category = Category(en_name=item['en_name'] , ru_name=item['ru_name'])
        category.save()
    clothes_instance = Category.objects.get(en_name='Clothes')
    
    for item in clothes_category:
        category = Category(parent_category=clothes_instance, en_name=item['en_name'] , ru_name=item['ru_name'])
        category.save()

def insert_color():
    for item in colors_list:
        color = ProductColor(en_value=item['en_color'], ru_value=item['ru_color'])
        color.save()

def insert_size():
    for item in sizes_list:
        size = ProductSize(value=item['type'])
        size.save()

def insert_group():
    for item in groups_list:
        group = ProductGroup(group_id=item['group_id'], description=item['description'])
        group.save()

def insert_product():
    for item in products_list:
        color = ProductColor.objects.get(ru_value=item['color'])
        cat = Category.objects.get(ru_name=item['category'])
        group = ProductGroup.objects.get(group_id=item['group'])
        product = Product(id=item['id'],
                          name=item['name'],
                          img_base=item['img_base'],
                          img_hover=item['img_hover'], 
                          img_details_1=item['img_details_1'],
                          img_details_2=item['img_details_1'],
                          category=cat,
                          color_attribute=color,
                          group=group,
                          )
        product.save()


def insert_product_sku():
    sizes = ['L', 'M', 'S']
    for item in product_sku_list:
        for size in sizes:
            product_sku = ProductSKU(
                id = item['product'] + size,
                product = Product.objects.get(id=item['product']),
                size_attribute = ProductSize.objects.get(value=size),
                price = item['price'],
                quantity = item['quantity']
            )
            product_sku.save()

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        # ids = [1,2,3,10,11,12]
        # for id in ids:
        #     instance = Category.objects.get(id=id)
        #     instance.delete()
        insert_category()
        insert_color()
        insert_size()
        insert_group()
        insert_product()
        insert_product_sku()
        # pass