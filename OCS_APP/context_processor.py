from OCS_APP.models import Category

def default(request):
    categories = Category.objects.all()
    return {'categories':categories,}