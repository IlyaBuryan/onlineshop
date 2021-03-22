from .models import Category

def cat_list(request):
    categories_list = Category.objects.all()

    return {'categories_list': categories_list}

