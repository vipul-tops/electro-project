from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('seller-index/',views.seller_index,name='seller-index'),
    path('about/',views.about,name='about'),
    path('term-condition/',views.term_condition,name='term-condition'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('change-password/',views.change_password,name='change-password'),
    path('edit-profile/',views.edit_profile,name='edit-profile'),
    path('shop/',views.shop,name='shop'),
    path('product-details/<int:pk>/',views.product_details,name='product-details'),
    path('add-to-wishlist/<int:pk>/',views.add_to_wishlist,name='add-to-wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove-from-wishlist/<int:pk>/',views.remove_from_wishlist,name='remove-from-wishlist'),
    path('add-to-cart/<int:pk>/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.cart,name='cart'),
    path('remove-from-cart/<int:pk>/',views.remove_from_cart,name='remove-from-cart'),
    path('change-qty/',views.change_qty,name='change-qty'),
    path('create-checkout-session/', views.create_checkout_session, name='payment'),
    path('success.html/', views.success,name='success'),
    path('cancel.html/', views.cancel,name='cancel'),
    path('myorder/',views.myorder,name='myorder'),
 

    path('laptop/',views.laptop,name='laptop'),
    path('camera/',views.camera,name='camera'),
    path('accessories/',views.accessories,name='accessories'),
    path('store/',views.store,name='store'),


    #seller
    path('seller-add-product/',views.seller_add_product,name='seller-add-product'),
    path('seller-view-product/',views.seller_view_product,name='seller-view-product'),
    path('seller-product-details/<int:pk>/',views.seller_product_details,name='seller-product-details'),
    path('seller-edit-product/<int:pk>/',views.seller_edit_product,name='seller-edit-product'),
    path('seller-delete-product/<int:pk>/',views.seller_delete_product,name='seller-delete-product'),
    path('seller-view-laptop/',views.seller_view_laptop,name='seller-view-laptop'),
    path('seller-view-camera/',views.seller_view_camera,name='seller-view-camera'),
    path('seller-view-accessories/',views.seller_view_accessories,name='seller-view-accessories'),
    path('seller-order/',views.seller_order,name='seller-order'),

    path('ajax/validate_email/',views.validate_email,name='validate_email'),
    path('ajax/validate_oldpassword/',views.validate_oldpassword,name='validate_oldpassword'),
    # path('ajax/validate_newpassword/',views.validate_newpassword,name='validate_newpassword'),
    path('ajax/validate_product_name/',views.validate_product_name,name='validate_product_name'),
]