from django.urls import path



from . import views
from django.urls import path
from .views import toggle_wishlist, wishlist_page, show_wishlist
from django.urls import path
from .views import download_invoice
from .views import viewbooking
from django.contrib.auth import views as auth_views
from django.urls import path



urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('showusers/', views.showuser, name='showuser'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('<int:prd_id>/productremove/',views.removeproduct, name='removeproduct'),
    path('<int:user_id>/removeuser/', views.removeuser, name='removeuser'),
    path('showcart/', views.showcart, name='showcart'),
    path('<int:prd_id>/mycart', views.mycart, name='mycart'),
    path('<int:cart_id>/removecart', views.removecart, name='removecart'),




    path('booking/<int:product_id>/', views.viewbooking, name='viewbooking'),


    path('addbooking/', views.getbookingdata, name='addbooking'),
    path('tracker/', views.tracker, name='tracker'),
    path('viewbymen/', views.viewbymen, name='viewbymen'),
    path('viewbywomen/', views.viewbywomen, name='viewbywomen'),
    path('<int:prdid>updateproduct/', views.updateproduct, name='updateproduct'),
    path('updatebookingstatus', views.updatebookingstatus, name='updatebookingstatus'),
    path('show_wishlist/', views.show_wishlist, name='show_wishlist'),
    path('wishlist/toggle/<int:prd_id>/', toggle_wishlist, name='toggle_wishlist'),
    path('show_wishlist/<int:prd_id>/', views.show_wishlist, name='show_wishlist'),



    path('booking/<int:product_id>/', views.viewbooking, name='booking_page'),



    path('show_cart/', views.show_cart, name='show_cart'),

    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('cart_booking/', views.cart_booking, name='cart_booking'),
    path('cartproductspayment/', views.CartProductsPayment, name='cart_products_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    # path('single_product_payment/<int:product_id>/', views.SingleProductPayment, name='single_product_payment'),
    path('download-invoice/<int:order_id>/', download_invoice, name='download_invoice'),
    path('OrderSuccess/', views.OrderSuccess, name='OrderSuccess'),

    path('track',views.track,name='track'),
    path('forgot', views.forgot_password),
    path('reset_password/<token>', views.reset_password),






]

