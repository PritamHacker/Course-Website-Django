from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . models import *
from django.contrib import messages

# Create your views here.
def index(request):
    # return HttpResponse('Hello World')
    #return render(request,'xyz/index.html',{})
    fcourse = Fcourse.objects.all()
    cat1 = Cat1.objects.all()
    cat2 = Cat2.objects.all()
    cat3 = Cat3.objects.all()
    if 'email' in request.session:
        user = Register.objects.filter(email=request.session['email']).first()
    else:
        user=''
    data={'title':'Home | Coursemela','user':user,'fcourse':fcourse,'cat1':cat1,'cat2':cat2,'cat3':cat3}
    return render(request,'index.html',data)

def signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        gender = request.POST['gender']
        # column_name = form_name
        if password == cpassword:
            checkemail = Register.objects.filter(email=email).first()
            if checkemail is not None:
                return HttpResponse('This email Already Register')
            else:
                data = Register.objects.create(fname=fname,lname=lname,phone=phone,email=email,password=password,gender=gender)
                return HttpResponse('Password Not Match with Confirm Password')   
        else:
            return HttpResponse('Registration UnSuccessfully')
    return render(request,'signup.html')

def regis(request):
    li=Register.objects.all()
    #li=Register.objects.filter(status=1)
    return render(request,'table.html',{'data':li})

def edit_user(request,id):
    # .first() .last() .filter
    user=Register.objects.get(id=id)
    data={'title':'Edit | Coursemela','user':user}
    return render(request,'edit.html',data)

def delete_user(request,id):
    user=Register.objects.get(id=id)
    #user.delete()
    user.status=0
    user.save()
    return redirect('regis')

def update(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        gender = request.POST['gender']
        id = request.POST['edit_id']
        user=Register.objects.get(id=id)
        user.fname=fname
        user.lname=lname
        user.phone=phone
        user.email=email
        user.password=password
        user.save()
        # column_name = form_name
    return redirect('regis')

def retrive_user(request,id):
    user=Register.objects.get(id=id)
    #user.delete()
    user.status=1
    user.save()
    return redirect('regis')

def login(request):
    data={'title':'Login | Coursemela'}
    return render(request,'login.html',data)

def loginsuccess(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        users = Register.objects.filter(email=email,password=password).first()
        if users is not None:
            request.session['email']=email # to set session
            messages.add_message(request,messages.SUCCESS,'login Successfull')
            # request.coockies['email']=email
            return redirect('index')
        else:
            messages.add_message(request,messages.ERROR,'logout Successfull')
            return redirect('login')

def logout(request):
    del request.session['email']
    messages.add_message(request,messages.SUCCESS,'logout Successfull')
    return redirect('index')

# My Code -------------------------------

def add_to_cart(request, product_type, product_id):
    product = None
    if product_type == 'fcourse':
        product = get_object_or_404(Fcourse, id=product_id)
    elif product_type == 'cat1':
        product = get_object_or_404(Cat1, id=product_id)
    elif product_type == 'cat2':
        product = get_object_or_404(Cat2, id=product_id)
    if product and 'email' in request.session:
        user = Register.objects.filter(email=request.session['email']).first()
        if user:
            cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
            messages.add_message(request,messages.SUCCESS,'Added to Cart')
            # if not created:
            #     cart_item.quantity += 1
            #     cart_item.save()
    return redirect('index')

# def qty_less(request, cart_item_id):
#     cart_item = get_object_or_404(CartItem, id=cart_item_id)
#     # cart_item.delete()
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()
#     return redirect('cart:cart')

# def qty_up(request, cart_item_id):
#     cart_item = get_object_or_404(CartItem, id=cart_item_id)
#     # cart_item.delete()
#     if cart_item.quantity >= 1:
#         cart_item.quantity += 1
#         cart_item.save()
#     # else:
#     #     cart_item.delete()
#     return redirect('cart:cart')

def del_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    messages.add_message(request,messages.SUCCESS,'Deleted Successfully')
    return redirect('cart')

def cart(request):
    if 'email' in request.session:
        user = Register.objects.filter(email=request.session['email']).first()
        if user:
            cart_items = CartItem.objects.filter(user=user)
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            # cart_items = CartItem.objects.all()
        data={'title':'Cart | Coursemela','cart_items': cart_items,'total_price':total_price}
    else:
        data = {'title':'Cart | Coursemela'}
    return render(request, 'cart.html',data)

def buy_now(request):
    if 'email' in request.session:
        user = Register.objects.filter(email=request.session['email']).first()
        if user:
            cart_items = CartItem.objects.filter(user=user)
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            if cart_items:
                order = Order.objects.create(user=user, total_price=total_price)
                for cart_item in cart_items:
                    OrderedItem.objects.create(user=user,order=order, product=cart_item.product)
                cart_items.delete()
                messages.add_message(request,messages.SUCCESS,'Successfully Ordered')
    return redirect('order_history')

def order_history(request):
    if 'email' in request.session:
        user = Register.objects.filter(email=request.session['email']).first()
        if user:
            orders = Order.objects.filter(user=user).order_by('-created_at')
            return render(request, 'order_history.html', {'orders': orders})
    return redirect('index')