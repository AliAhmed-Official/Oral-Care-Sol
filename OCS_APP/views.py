from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_control
from OCS_APP.models import CartOrder, CartOrderItems, Category, Address, Product, ProductReview
from userauths.models import Profile
from django.contrib import messages
from django.db.models import Avg, Count
from django.db.models.functions import ExtractMonth
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator
import calendar
from OCS_APP.forms import ProductReviewForm, ProductFilterForm

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    products = Product.objects.filter(product_status = 'published', featured = True).exclude(stock = 0).order_by('-id')
    return render(request, 'index.html', {'products':products})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def category_list_view(request):
    categories = Category.objects.all()
    categories_to_delete = []
    for category in categories:
        products_count = Product.objects.filter(product_status='published', category=category).exclude(stock = 0).count()
        if products_count == 0:
            categories_to_delete.append(category)
    categories = categories.exclude(pk__in=[category.pk for category in categories_to_delete])
    return render(request, 'category-list.html', {'categories':categories, 'products_count':products_count})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def category_products_list_view(request, cid):
    category = Category.objects.get(cid = cid)
    products = Product.objects.filter(product_status = 'published', category = category).exclude(stock = 0)
    return render(request, 'category-product-list.html', {'category':category,'products':products})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_detail_view(request, pid):
    product = Product.objects.get(pid = pid)
    range_for_template = range(1, product.stock + 1)
    products = Product.objects.filter(category = product.category).exclude(pid = pid)
    products = products.exclude(stock = 0)
    reviews = ProductReview.objects.filter(product = product).order_by('-date')
    average_rating = ProductReview.objects.filter(product = product).aggregate(rating = Avg('rating'))
    review_form = ProductReviewForm()
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user = request.user, product = product).count()
        if user_review_count > 0:
            make_review = False
    p_image = product.p_images.all()
    return render(request, 'product-detail.html', {'product':product,'products':products,'p_image':p_image, 'range_for_template':range_for_template, 'reviews':reviews, 'average_rating':average_rating, 'review_form':review_form, 'make_review':make_review})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def tag_list(request, tag_slug = None):
    products = Product.objects.filter(product_status = 'published').exclude(stock = 0).order_by('-id')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    return render(request, 'tag.html', {'products':products,'tag':tag})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_view(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains = query).exclude(stock = 0).order_by("-date")
    return render(request, 'search.html', {'products':products,'query':query})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart_view(request):
    try:
        if len(request.session['cart_data_obj']) == 0:
            return redirect('OCS_APP:index')
    except KeyError:
        return redirect('OCS_APP:index')
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for item in request.session['cart_data_obj'].values():
            cart_total_amount += int(item['qty']) * int(item['price'])
        return render(request, 'cart.html', {'cart_data':request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, 'Your cart is empty')
        return redirect('OCS_APP:index')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    cart_data = request.session['cart_data_obj']
    del cart_data[product_id]
    request.session['cart_data_obj'] = cart_data
    updated_cart_total_amount = 0
    for item in request.session['cart_data_obj'].values():
        updated_cart_total_amount += int(item['qty']) * float(item['price'])
    return JsonResponse({'updated_cart_total_amount':updated_cart_total_amount, 'totalitems':len(request.session['cart_data_obj'])})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['product_quantity']
    cart_data = request.session['cart_data_obj']
    cart_data[product_id]['qty'] = product_qty
    updated_price = float(cart_data[product_id]['price']) * int(product_qty)
    request.session['cart_data_obj'] = cart_data
    updated_cart_total_amount = 0
    for item in request.session['cart_data_obj'].values():
        updated_cart_total_amount += int(item['qty']) * float(item['price'])
    return JsonResponse({'updated_price':updated_price, 'updated_cart_total_amount':updated_cart_total_amount})
    
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkout_view(request):
    try:
        if len(request.session['cart_data_obj']) == 0:
            return redirect('OCS_APP:index')
    except KeyError:
        return redirect('OCS_APP:index')
    cart_total_amount = 0
    active_address = None
    if 'cart_data_obj' in request.session:
        for item in request.session['cart_data_obj'].values():
            cart_total_amount += int(item['qty']) * float(item['price'])
    try:
        active_address = Address.objects.get(user = request.user, status = True)
    except:
        active_address = None
    address = Address.objects.filter(user = request.user)
    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        if address != None and mobile != None:
            Address.objects.create(user = request.user, address = address, mobile = mobile)
            messages.success(request, 'Address added successfully.')
            return redirect('OCS_APP:checkout')
        else:
            if not active_address:
                messages.warning(request, 'Please add or select one address.')
                return redirect('OCS_APP:checkout')
            pay_method = request.POST.get('payment_method')
            order = CartOrder.objects.create(user = request.user, price = cart_total_amount, delivery_address = active_address.address, payment_method = pay_method)
            for id, item in request.session['cart_data_obj'].items():
                CartOrderItems.objects.create(order = order, invoice_no = order.id, item = item['title'], image = item['image'], qty = item['qty'], price = item['price'], total = float(item['qty']) * float(item['price']))
                pro = Product.objects.get(id = id)
                pro.stock -= int(item['qty'])
                pro.save()
            send_order_confirmation_email(order, pay_method, active_address)
            if pay_method == 'Cash On Delivery':
                return redirect('OCS_APP:payment-completed', inv_id=str(order.id), pay_method=pay_method) 
            elif pay_method == 'Credit Card':
                pass
            else:
                messages.warning(request, 'Invalid Payment Method!')
                return redirect('OCS_APP:checkout')
    return render(request, 'checkout.html', {'cart_data':request.session['cart_data_obj'], 'cart_total_amount':cart_total_amount, 'address':address})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment_completed_view(request, inv_id, pay_method):
    invoice_items = CartOrderItems.objects.filter(invoice_no=int(inv_id))
    obj = CartOrder.objects.filter(id = inv_id)
    cart_total_amount = 0
    for i in invoice_items:
        cart_total_amount += int(i.qty) * float(i.price)
    try:
        active_address = Address.objects.get(user = request.user, status = True)
    except:
        active_address = None
    request.session['cart_data_obj'] = {}
    return render(request, 'payment-completed.html', {'cart_data':invoice_items, 'cart_total_amount':cart_total_amount, 'active_address':active_address, 'invoice_no':inv_id, 'pay_method': pay_method, 'cus_name':obj[0].user.username, 'cus_email':obj[0].user.User_Email})

def send_order_confirmation_email(order, pay_method, active_address):
    subject = 'Order Confirmation From Oral Care Solution'
    order_items = CartOrderItems.objects.filter(invoice_no=order.id)
    html_message = render_to_string('order_confirmation_email.html', {'name':order.user.username, 'order_items': order_items, 'pay_method':pay_method, 'active_address':active_address, 'total':order.price})
    plain_message = strip_tags(html_message)
    from_email = 'aliahmedchamp@gmail.com'
    to_email = order.user.User_Email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status = False)
    Address.objects.filter(id = id).update(status = True)
    return JsonResponse({"boolean":True})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_address(request):
    id = request.GET['id']
    address = Address.objects.filter(id = id)
    address.delete()
    return JsonResponse({"boolean":True})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment_failed_view(request):
    return render(request, 'payment-failed.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_to_cart(request):
    cart_product = {}
    q = request.GET['qty']
    if q == '' or q == '0':
        q = '1'
    x = Product.objects.get(id = str(request.GET['id']))
    initialstock = x.stock
    cart_product[str(request.GET['id'])] = {'title': request.GET['title'], 'qty': q, 'price': request.GET['price'], 'image': request.GET['image'], 'max_stock_product':initialstock, 'pid': request.GET['pid']}
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], "totalcartitems":len(request.session['cart_data_obj'])})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user = request.user).order_by("-id")
    orders = CartOrder.objects.annotate(month = ExtractMonth('order_date')).values('month').annotate(count = Count('id')).values('month', 'count')
    month = []
    total_orders = []
    for i in orders:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i['count'])
    profile = Profile.objects.get(user = request.user)
    return render(request, 'dashboard.html', {'orders_list':orders_list, 'profile':profile, 'orders':orders, 'month':month, 'total_orders':total_orders})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_detail(request, id):
    order = CartOrder.objects.get(user = request.user, id = id)
    order_items = CartOrderItems.objects.filter(order = order)
    obj = Address.objects.filter(user = request.user, address = order.delivery_address)
    for i in obj:
        a = i.mobile
    return render(request, 'order-detail.html', {'order_items':order_items, 'id':id, 'total':order.price, 'number':order.id, 'date':str(order.order_date.date()), 'email':order.user.User_Email, 'name':order.user.username, 'delivery_add':order.delivery_address, 'phone':a, 'pay_method':order.payment_method})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        telephone = request.POST.get('telephone')
        subject = f"Message From Customer: {name}, ({email}), ({telephone})"
        body = message
        send_mail(subject, body, email, [f'aliahmedchamp@gmail.com'])
    return render(request, 'Contact_us.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def shop_view(request):
    form = ProductFilterForm(request.GET)
    if form.is_valid():
        cat_id = form.cleaned_data['category']
        manu_id = form.cleaned_data['manufacturer']
        if cat_id == 'no-cat' and manu_id == 'no-manu':
            products = Product.objects.filter(product_status='published').exclude(stock=0).order_by('-id')
        elif cat_id == '' and manu_id == '':
            products = Product.objects.filter(product_status='published').exclude(stock=0).order_by('-id')
        elif cat_id == 'no-cat':
            products = Product.objects.filter(product_status='published', manufacturer=manu_id).exclude(stock=0).order_by('-id')
        elif manu_id == 'no-manu':
            products = Product.objects.filter(product_status='published', category=cat_id).exclude(stock=0).order_by('-id')
        else:
            products = Product.objects.filter(product_status='published', category=cat_id, manufacturer=manu_id).exclude(stock=0).order_by('-id')
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop.html', {'page_obj': page_obj, 'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ajax_add_review(request, pid):
    product = Product.objects.get(pk = pid)
    user = request.user
    ProductReview.objects.create(user = user, product = product, review = request.POST['review'], rating = request.POST['rating'])
    average_reviews = ProductReview.objects.filter(product = product).aggregate(rating = Avg('rating'))
    count_review = ProductReview.objects.filter(product = product).count()
    return JsonResponse({'bool':True, 'context':{'user':user.username, 'review':request.POST['review'], 'rating':request.POST['rating']}, 'average_reviews':average_reviews, 'count_review':count_review})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def my(request):
    return render(request, 'my.html')