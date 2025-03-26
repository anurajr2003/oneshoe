from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Wishlist, Product
from django.contrib import messages # type: ignore
import razorpay
from django import forms
from .forms import *
from django.db import connection




# Create your views here.

def track(request):

    return render(request,'track.html')




def index(request):
    proobj = Product.objects.all()
    products = Product.objects.all()
    menobj = Product.objects.filter(category='MEN')
    womenobj = Product.objects.filter(category='WOMEN')
    if request.session.has_key('user_id'):
        userobj = request.session['user_id']
        logobj = Login.objects.get(pk=userobj)
        userobjs = User.objects.get(loginid=logobj)
        cartobj = Cart.objects.filter(user_id=logobj).count()
        return render(request, 'index.html', {'user_info': userobjs, 'pros': proobj,'cartitems':cartobj,'mens': menobj, 'womens': womenobj})
    return render(request, 'index.html', {'user_info': False, 'pros': proobj,'mens': menobj, 'womens': womenobj})
    return render(request, "index.html", {"products": products})
    for product in products:
        print(f"Product ID: {product.id}")  # Check if IDs exist


def dashboard(request):
    proobj = Product.objects.all()[:10]
    userobj = User.objects.all()
    bookingobj = Booking.objects.exclude(status='Delivered')
    bookitems = Bookingitem.objects.all()
    bookaddress = BookingAddress.objects.all()
    totalorders = Booking.objects.all().count()
    return render(request, 'adminhome/dashboard.html',{'bookaddress':bookaddress,'bookitems': bookitems,'pro': proobj, 'user': userobj,'bookings':bookingobj,'totalorders': totalorders})


def removeproduct(request, prd_id):
    try:
        proobj = Product.objects.get(pk=prd_id)
    except:
        return dashboard(request)
    else:
        proobj.delete()
    return dashboard(request)


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')

        if username == 'admin' and password == 'admin':
            return dashboard(request)
        else:
            if Login.objects.filter(username=username, password=password).exists():
                logobj = Login.objects.get(username=username, password=password)
                request.session['user_id'] = logobj.id
                userobj = User.objects.get(loginid=logobj.id)
                return index(request)
            else:
                return HttpResponse("Wrong Password or Username")
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        paword = request.POST.get('password')
        loginobj = Login()
        loginobj.username = uname
        loginobj.password = paword
        loginobj.save()

        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        regobj = User()
        regobj.loginid = loginobj
        regobj.fname = fname
        regobj.lname = lname
        regobj.email = email
        regobj.gender = gender
        regobj.isapprove = True
        regobj.isdelete = False
        regobj.save()
        return render(request, 'login.html')
    return render(request, 'register.html')


def logout(request):
    try:
        del request.session['user_id']
    except:
        return index(request)
    return render(request, 'index.html')


def showuser(request):
    userobj = User.objects.all()
    return render(request, 'adminhome/userdetails.html', {'userinfo':userobj})


def removeuser(request, user_id):
    try:
        userobj = Login.objects.get(pk=user_id)
    except:
        return showuser(request)
    else:
        userobj.delete()
        return showuser(request)


def addproduct(request):
    if request.method == "POST":
        productname = request.POST.get('pname')
        brandname = request.POST.get('bname')
        material = request.POST.get('leather')
        colour = request.POST.get('color')
        price = request.POST.get('price')
        category = request.POST.get('category')
        producttype = request.POST.get('ptype')
        size = request.POST.get('size')
        image = request.FILES['image']
        qty = request.POST.get('stock')

        proobj = Product()
        proobj.productname = productname
        proobj.brandname = brandname
        proobj.material = material
        proobj.colour = colour
        proobj.price = price
        proobj.quantity = qty
        proobj.category = category
        proobj.producttype = producttype
        proobj.image = image
        proobj.size = size
        proobj.save()
        return dashboard(request)
    return render(request, 'adminhome/addproduct.html')


from .models import User, Cart, Product, Login  # Ensure Login model is imported

def showcart(request):
    if 'user_id' not in request.session:
        return redirect('login')

    logobj = Login.objects.get(pk=request.session['user_id'])
    cart_items = Cart.objects.filter(user_id=logobj).select_related('prd_id')

    total_price = sum(item.prd_id.price * item.qty for item in cart_items)

    request.session['cart_total'] = total_price  # ✅ Store total in session

    return render(request, 'cart.html', {'carts': cart_items, 'total': total_price})

def viewbooking(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    total_amount = product.price

    return render(request, 'booking.html', {
        'product': product,
        'total_amount': total_amount
    })


from django.contrib.auth.decorators import login_required





def mycart(request, prd_id):
    if not prd_id:
        print("Error: Received an empty prd_id!")
        return redirect('show_wishlist')  # Redirect to wishlist if prd_id is invalid

    if request.session.has_key('user_id'):
        logobj = Login.objects.get(pk=request.session['user_id'])
        prdobj = get_object_or_404(Product, pk=prd_id)

        if Cart.objects.filter(prd_id=prdobj, user_id=logobj).exists():
            messages.warning(request, "Item already in Cart")
        else:
            cartobj = Cart(user_id=logobj, prd_id=prdobj)
            cartobj.save()
            messages.success(request, "Item added to cart!")

    else:
        return render(request, 'login.html')

    return redirect('show_cart')

def removecart(request, cart_id):
    cartobj = Cart.objects.get(pk=cart_id)
    cartobj.delete()
    return showcart(request)


# def viewbooking(request):
#     return render(request, 'booking.html')



def getbookingdata(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        country = request.POST.get('country')

        cartobj = Cart.objects.filter(user_id=request.session['user_id'])
        totalmoney = 0

        try:
            for cart in cartobj:
                itemobj = Product.objects.get(id=cart.prd_id_id)
                itemobj.quantity -= 1
                itemobj.save()
        except:
            return HttpResponse("Sorry something went wrong")
        else:

            for cart in cartobj:
                totalmoney += cart.prd_id.price


            obj1 = Booking()
            obj1.user_id = Login.objects.get(id=request.session['user_id'])
            obj1.totalprice = totalmoney
            obj1.save()

            for cart in cartobj:
                obj2 = Bookingitem()
                obj2.booking_id = obj1
                obj2.product_id = Product.objects.get(id=cart.prd_id_id)
                obj2.save()

            obj3 = BookingAddress()
            obj3.booking_id = obj1
            obj3.address = address
            obj3.country = country
            obj3.pincode = pincode
            obj3.state = state
            obj3.phone = phone
            obj3.email = email
            obj3.save()

            cartobj.delete()

            return index(request)


def viewbymen(request):
    proobj = Product.objects.filter(category='MEN')
    if request.session.has_key('user_id'):
        userobj = request.session['user_id']
        logobj = Login.objects.get(pk=userobj)
        userobjs = User.objects.get(loginid=logobj)
        cartobj = Cart.objects.filter(user_id=logobj).count()
        return render(request, 'index.html', {'user_info': userobjs, 'pros': proobj,'cartitems':cartobj})
    return render(request, 'index.html', {'user_info': False, 'pros': proobj})


def viewbywomen(request):
    proobj = Product.objects.filter(category='WOMEN')
    if request.session.has_key('user_id'):
        userobj = request.session['user_id']
        logobj = Login.objects.get(pk=userobj)
        userobjs = User.objects.get(loginid=logobj)
        cartobj = Cart.objects.filter(user_id=logobj).count()
        return render(request, 'index.html', {'user_info': userobjs, 'pros': proobj,'cartitems':cartobj})
    return render(request, 'index.html', {'user_info': False, 'pros': proobj})


from django.shortcuts import render, redirect
from .models import Login, User, Bookingitem

def tracker(request):
    if request.session.has_key('user_id'):

        try:
            # Get the logged-in user
            logobj = Login.objects.get(id=request.session['user_id'])
            user = User.objects.get(loginid=logobj)

            # Fetch all booking items for the user
            bookings = Bookingitem.objects.filter(user_details=user)
            book=BookingAddress.objects.filter(userdetails=user)

            print(book)
            if bookings.exists():
                return render(request, 'tracker.html', {'books': bookings})

            return render(request, 'tracker.html', {'message': "No bookings found!"})

        except Login.DoesNotExist:
            return redirect('login_url_name')  # Redirect to login if session is invalid

    return redirect('login_url_name')  # Redirect to login if session is missing



def updateproduct(request, prdid):
    prdobj = Product.objects.get(id=prdid)
    if request.method == 'POST':
        pname = request.POST.get('pname')
        bname = request.POST.get('bname')
        size = request.POST.get('size')
        types = request.POST.get('leather')
        color = request.POST.get('color')
        price = request.POST.get('price')
        category = request.POST.get('category')
        ptype = request.POST.get('ptype')
        qty = request.POST.get('stock')
        try:
            img = request.FILES['image']
        except:
            pass
        else:
            prdobj.image = img
            prdobj.save()

        prdobj.productname = pname
        prdobj.brandname = bname
        prdobj.size = size
        prdobj.quantity = qty
        prdobj.material = types
        prdobj.colour = color
        prdobj.price = price
        prdobj.producttype = ptype
        prdobj.category = category
        prdobj.save()

        return dashboard(request)

    return render(request, 'adminhome/updateproduct.html',{'prd': prdobj})


def updatebookingstatus(request):
    if request.method == 'POST':
        bookid = request.POST.get('bookid')
        status = request.POST.get('status')
        print("book id",bookid,"status",status)
        bookobj = Bookingitem.objects.get(pk=bookid)
        bookobj.order_status = status
        bookobj.save()

        return dashboard(request)

from .models import Wishlist, Product

def toggle_wishlist(request, prd_id):
    if not request.session.has_key('user_id'):
        return JsonResponse({'status': 'login_required'})

    logobj = User.objects.get(loginid=request.session['user_id'])
    product = Product.objects.get(id=prd_id)

    wishlist_item, created = Wishlist.objects.get_or_create(user=logobj, product=product)

    if not created:
        wishlist_item.delete()
        return JsonResponse({'status': 'removed'})

    return JsonResponse({'status': 'added'})


def show_wishlist(request, prd_id=None):
    if not request.session.has_key('user_id'):
        return redirect('login')

    logobj = User.objects.get(loginid=request.session['user_id'])

    if prd_id:  # Add product to wishlist if provided
        product = Product.objects.get(id=prd_id)
        Wishlist.objects.get_or_create(user=logobj, product=product)

    wishlist_items = Wishlist.objects.filter(user=logobj)

    return render(request, 'wishlist.html', {'wishlist': wishlist_items})


@login_required
def wishlist_page(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist': wishlist_items})





from django.shortcuts import render, get_object_or_404
from .models import Product

from django.shortcuts import render, get_object_or_404
from .models import Cart, Product


def booking_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Calculate cart total price
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user_id=request.user.id)
        total_price = sum(item.prd_id.price * item.qty for item in cart_items)
    else:
        total_price = 0  # Handle case where user is not logged in

    return render(request, 'booking.html', {
        'product': product,
        'total_amount': total_price,  # Pass the total price to the template
    })



import razorpay
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


import json
from django.http import JsonResponse
from django.conf import settings
import razorpay

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



from .models import Cart, Login

def show_cart(request):
    if request.session.has_key('user_id'):
        logobj = Login.objects.get(pk=request.session['user_id'])
        cart_items = Cart.objects.filter(user_id=logobj).select_related('prd_id')

        # Debug: Print cart items
        for item in cart_items:
            print(f"Product: {item.prd_id.productname}, Quantity: {item.qty}, Price: {item.prd_id.price}")

        total_amount = sum(item.prd_id.price * item.qty for item in cart_items)
        return render(request, 'cart.html', {'carts': cart_items, 'total': total_amount})
    else:
        return render(request, 'login.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Booking, Product

def booking_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    total_amount = product.price  # Calculate total amount if needed
    return render(request, 'booking.html', {'product': product, 'total_amount': total_amount})

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return redirect('profile')


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, UserCarts, ProductsOrders, Product
import razorpay
import random
from datetime import datetime

def ProductsPayment(request, i):
    i *= 100  # Convert to paise for Razorpay

    user = User.objects.get(username=request.session['user'])
    if request.method == 'POST':
        # Handle address form submission if needed
        return render(request, 'user/order_product/payment.html',
                      {'user': request.session['user'], 'flag': 0, 'price': i, 'p': int(i / 100)})

    # Initialize Razorpay client
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': i, 'currency': 'INR', 'payment_capture': '1'})

    return render(request, 'user/order_product/payment.html',
                  {'user': request.session['user'], 'flag': 1, 'price': i, 'p': int(i / 100), 'payment': payment})

def OrderSuccess(request):
    # Get the current user
    user = User.objects.get(username=request.session['user'])

    # Fetch all items in the user's cart
    data = UserCarts.objects.filter(user_details=user)

    # Calculate total price
    total_price = 0
    for item in data:
        total_price += int(item.product_details.price) * item.quantity

    # Prepare the list of products and create orders
    ordered_products = []
    for item in data:
        product_total_price = int(item.product_details.price) * item.quantity

        # Generate a random 4-digit number
        random_number = random.randint(1000, 9999)
        # Create a new order for each product in the cart
        ProductsOrders.objects.create(
            user_details=user,
            product_details=item.product_details,
            payment_amount=product_total_price,
            quantity=item.quantity,
            payment_status='success',
            product_code=random_number, created_at=datetime.now()
        )
        p = Product.objects.get(pk=item.product_details.pk)
        p.quantity -= item.quantity
        p.save()

        # Add product info to the ordered products list
        ordered_products.append({
            'product_name': item.product_details.productname,
            'product_quantity': item.quantity,
            'total_price': product_total_price,
            'product_code': random_number
        })

    # Clear the user's cart after the order is placed
    UserCarts.objects.filter(user_details=user).delete()

    # Render the invoice page
    return render(request, "user/order_product/ProductsInvoice.html", {
        'user': request.session['user'],
        'data': data,
        'list': ordered_products,
        'total': total_price,
        'address': user.housename if hasattr(user, 'housename') else '',
        'landmark': user.landmark if hasattr(user, 'landmark') else '',
        'area': user.area if hasattr(user, 'area') else '',
        'pincode': user.pincode if hasattr(user, 'pincode') else '',
    })

from django.shortcuts import render, redirect
from .models import Cart, Login

def cart_booking(request):
    if request.session.has_key('user_id'):
        logobj = Login.objects.get(pk=request.session['user_id'])
        cart_items = Cart.objects.filter(user_id=logobj)
        total_amount = sum(item.prd_id.price * item.qty for item in cart_items)

        return render(request, 'cart_booking.html', {
            'cart_items': cart_items,
            'total_amount': total_amount,
        })
    else:
        return redirect('login')  # Redirect to login if the user is not logged in
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cart, Product, Login, User, BookingAddress
import razorpay

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cart, Product, Login, User, BookingAddress
import razorpay

def CartProductsPayment(request):
    # Calculate the total amount of all items in the cart
    total_amount=0
    if request.session.has_key('user_id'):
        logobj = Login.objects.get(pk=request.session['user_id'])
        cart_items = Cart.objects.filter(user_id=logobj)
        total_amount = sum(item.prd_id.price * item.qty for item in cart_items) * 100  # Convert to paise
    else:
        return redirect('login')  # Redirect to login if the user is not logged in

    logobj = Login.objects.get(pk=request.session['user_id'])
    user = User.objects.get(loginid=logobj)
    print(user)

    if request.method == 'POST':
        # Get form data from the POST request
        address = request.POST.get('address')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Create a new BookingAddress object
        BookingAddress(

            userdetails=user,  # Use the correct field name (e.g., 'login' instead of 'user_id')
            address=address,
            country=country,
            pincode=pincode,
            state=state,
            email=email,
            phone=phone,
            total_amount=total_amount
        ).save()


        print('Address saved successfully')

        return render(request, 'payment.html', {
            'user': request.session['user_id'],
            'flag': 0,
            'price': total_amount,
            'p': int(total_amount / 100)
        })

    # Initialize Razorpay client
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': total_amount, 'currency': 'INR', 'payment_capture': '1'})  # Create Razorpay order

    return render(request, 'payment.html', {
        'user': request.session['user'],
        'flag': 1,
        'price': total_amount,
        'p': int(total_amount / 100)
    })
from django.shortcuts import render
from django.shortcuts import render


from .models import Cart, Login, ProductsOrders, Product

from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
import io

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get("payment_id")
        order_id = request.POST.get("order_id")
    elif request.method == "GET":
        payment_id = request.GET.get("payment_id")
        order_id = request.GET.get("order_id")
    else:
        return HttpResponse("Invalid request method", status=400)

    # Get user email from session or database
    user_email = request.user.email if request.user.is_authenticated else "test@example.com"

    # Generate Invoice PDF
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 750, "Invoice")
    pdf.drawString(100, 730, f"Payment ID: {payment_id}")
    pdf.drawString(100, 710, f"Order ID: {order_id}")
    pdf.drawString(100, 690, "Thank you for your purchase!")
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    # Send Invoice via Email
    # email = EmailMessage(
    #     "Your Payment Invoice",
    #     "Thank you for your payment. Find your invoice attached.",
    #     "yourshop@example.com",
    #     [user_email],
    # )
    # email.attach(f"Invoice_{order_id}.pdf", buffer.getvalue(), "application/pdf")
    # email.send()

    return render(request, "payment_success.html", {"payment_id": payment_id, "order_id": order_id})
    return render(request, 'payment_success.html', {'booking': booking})


from django.shortcuts import render

# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
# from .models import Product, Login, Booking, BookingAddress, Bookingitem
# import razorpay
#
# def SingleProductPayment(request, product_id):
#     print(f"Product ID: {product_id}")
#
#     # Fetch the product
#     product = get_object_or_404(Product, id=product_id)
#     total_amount = product.price * 100  # Convert to paise for Razorpay
#
#     # Fetch the logged-in user
#     if request.session.has_key('user_id'):
#         logobj = Login.objects.get(pk=request.session['user_id'])
#     else:
#         return redirect('login')  # Redirect to login if the user is not logged in
#
#     if request.method == 'POST':
#         # Get form data from the POST request
#         address = request.POST.get('address')
#         country = request.POST.get('country')
#         pincode = request.POST.get('pincode')
#         state = request.POST.get('state')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#
#         # Create a new Booking object
#         booking = Booking(
#             user_id=logobj,
#             totalprice=product.price,
#             status='Packing'
#         )
#         booking.save()
#
#         # Create a new Bookingitem object
#         booking_item = Bookingitem(pa
#             booking_id=booking,
#             product_id=product
#         )
#         booking_item.save()
#
#         # Create a new BookingAddress object
#         booking_address = BookingAddress(
#             userdetails=Login.objects.get(pk=request.session['user_id']),
#             address=address,
#             country=country,
#             pincode=pincode,
#             state=state,
#             email=email,
#             phone=phone
#         )
#         booking_address.save()
#
#         print('Booking and address saved successfully')
#
#         # Initialize Razorpay client
#         client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
#         payment = client.order.create({'amount': total_amount, 'currency': 'INR', 'payment_capture': '1'})
#
#         return render(request, 'payment1.html', {
#             'user': request.session['user'],
#             'flag': 1,
#             'price': total_amount,
#             'p': int(total_amount / 100),
#             'payment': payment
#         })
#
#     # Render the address form for single product payment
#     return render(request, 'single_product_payment.html', {
#         'product': product,
#         'total_amount': product.price
#     })

from django.http import FileResponse
from reportlab.pdfgen import canvas
import io

from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Booking

def download_invoice(request, order_id):
    booking = get_object_or_404(Booking, id=order_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{order_id}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Invoice Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Invoice")

    # Order Details
    p.setFont("Helvetica", 12)
    p.drawString(50, 750, f"Order ID: {booking.id}")
    p.drawString(50, 730, f"Customer: {booking.user_id.first_name} {booking.user_id.last_name}")
    p.drawString(50, 710, f"Total Amount: ₹{booking.totalprice}")
    p.drawString(50, 690, f"Status: {booking.status}")

    # Footer
    p.drawString(50, 650, "Thank you for shopping with us!")

    p.showPage()
    p.save()
    buffer.seek(0)

    response.write(buffer.read())
    return response


from django.shortcuts import render
from datetime import datetime
from .models import User, Cart, Bookingitem, Product

from django.shortcuts import render
from datetime import datetime
from .models import User, Cart, Bookingitem, Product

from django.shortcuts import render
from datetime import datetime
from .models import User, Cart, Bookingitem, Product


def OrderSuccess(request):
    print("Saving booking item for user:", User.id)

    print("order sucess")
    try:
        print("---- Order Success Function Called ----")  # ✅ Debug Start

        # Get the current user
        user = Login.objects.get(pk=request.session['user_id'])
        print("User Found:", user)
        u=User.objects.get(loginid=user)


        # Fetch all items in the user's cart
        cart_items = Cart.objects.filter(user_id=user)
        print("Cart Items:", list(cart_items))

        if not cart_items.exists():
            print("⚠️ No items in cart!")  # ✅ Empty cart check
            return render(request, "tracker.html", {'message': "Your cart is empty!"})

        total_price = 0
        ordered_products = []

        for item in cart_items:
            item_total = int(item.prd_id.price) * item.qty
            total_price += item_total

            print(f"📦 Creating order: {item.prd_id.productname} - Qty: {item.qty} - Price: {item_total}")

            # Create a new order
            booking = Bookingitem.objects.create(
                user_details=u,
                product_details=item.prd_id,
                quantity=item.qty,
                payment_amount=item_total,
                payment_status='success',
                order_status='ordered',
                created_at=datetime.now(),

            )
            print("✅ Order saved:", booking)

            # Reduce product stock
            item.prd_id.quantity -= item.qty
            item.prd_id.save()

            ordered_products.append({
                'product_name': item.prd_id.productname,
                'product_quantity': item.qty,
                'total_price': item_total,
            })

        # Clear the user's cart after order placement
        cart_items.delete()
        print("🛒 Cart cleared!")

        return render(request, "payment_success.html", {
            'user': u,
            'list': ordered_products,
            'total': total_price,
            'address': user.loginid.housename,
            'landmark': user.loginid.landmark,
            'area': user.loginid.area,
            'pincode': user.loginid.pincode,
        })

    except Exception as e:
        print(f"❌ Error in OrderSuccess: {e}")
        return render(request, "payment_success.html", {'error': "An error occurred while processing your order."})


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ProductsOrders

def place_order(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        payment_amount = float(request.POST.get('payment_amount'))
        payment_status = "Paid"  # Update based on payment verification

        # Create a new order
        order = ProductsOrders.objects.create(
            user_details=user,
            product_details_id=product_id,
            quantity=quantity,
            payment_amount=payment_amount,
            payment_status=payment_status
        )

        # Send order confirmation email
        send_mail(
            subject="Order Confirmation - Your Order Has Been Placed!",
            message=f"Dear {user.username},\n\nThank you for your order!\n\n"
                    f"Order Details:\n"
                    f"Product: {order.product_details.name}\n"
                    f"Quantity: {order.quantity}\n"
                    f"Total Amount: ${order.payment_amount}\n\n"
                    f"Your order is being processed and will be delivered soon.\n"
                    f"Thank you for shopping with us!\n\nBest regards,\nYour Shoe Shop Team",
            from_email="your-email@gmail.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_success_page')  # Update this to your success page URL

    return redirect('home')


from django.utils.crypto import get_random_string # type: ignore
from django.core.mail import send_mail # type: ignore

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except Exception as e:  # noqa: E722
            print(e)
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(User=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset_password/{token}'
        try:
            print("hiii")
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')
            print("hello")
        except Exception as e:
            print(e)# noqa: E722
            messages.info(request, "Network connection failed")
            return redirect(forgot_password)

    return render(request,'forgot.html')

def reset_password(request,token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.User.loginid.password=new_password
            print(password_reset.User.loginid.password)
            password_reset.User.loginid.save()
            # password_reset.delete()
            return redirect(login)
    return render(request, 'reset_password.html', {'token': token})