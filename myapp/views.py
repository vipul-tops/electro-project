from django.shortcuts import render,redirect
from .models import User,Product,Wishlist,Cart
import requests
import random
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://localhost:8000'

# Create your views here.

@csrf_exempt
def create_checkout_session(request):
	amount = int(json.load(request)['post_data'])
	final_amount=amount*100
	
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'product_data': {
					'name': 'Checkout Session Data',
					},
				'unit_amount': final_amount,
				},
			'quantity': 1,
			}],
		mode='payment',
		success_url=YOUR_DOMAIN + '/success.html',
		cancel_url=YOUR_DOMAIN + '/cancel.html',)
	return JsonResponse({'id': session.id})

def success(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	for i in carts:
		i.payment_status=True
		i.save()
		
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)
	return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')

def validate_email(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

def validate_oldpassword(request):
	oldpassword=request.GET.get('oldpassword')
	user=User.objects.get(email=request.session['email'])
	print(user.fname)
	print(oldpassword)
	data={
		'is_taken':User.objects.filter(password=oldpassword,email=user.email).exists()
	}
	return JsonResponse(data)

def validate_product_name(request):
	seller=User.objects.get(email=request.session['email'])
	product_name=request.GET.get('product_name')
	print(product_name)
	data={
		'is_taken':Product.objects.filter(seller=seller,product_name=product_name).exists()
	}
	return JsonResponse(data)

 # def validate_newpassword(request):
 # 	newpassword=request.GET.get('newpassword')
 # 	user=User.objects.get(email=request.session['email'])
 # 	data={
 # 		'is_taken':User.objects.filter(password=newpassword).exists()
 # 	}
 # 	return JsonResponse(data)

def index(request):
	products=list(Product.objects.all())
	random_products = random.sample(products, min(len(products), 3))
	random_product = random.sample(products, min(len(products), 8))
	random_productt = random.sample(products, min(len(products), 3))
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=="buyer":
			return render(request,'index.html',{'products':products,'random_products':random_products,'random_product':random_product,'random_productt':random_productt})

		else:
			return render(request,'seller-index.html',{'products':products,'random_products':random_products,'random_product':random_product,'random_productt':random_productt})

	except:
		return render(request,'index.html',{'products':products,'random_products':random_products,'random_product':random_product,'random_productt':random_productt})

def seller_index(request):
	products=list(Product.objects.all())
	random_products = random.sample(products, min(len(products), 3))
	random_product = random.sample(products, min(len(products), 8))
	random_productt = random.sample(products, min(len(products), 3))
	return render(request,'seller-index.html',{'products':products,'random_products':random_products,'random_product':random_product,'random_productt':random_productt})


def about(request):
	return render(request,'about.html')

def term_condition(request):
	return render(request,'term-condition.html')


def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:

				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					password=request.POST['password'],
					profile_pic=request.FILES['profile_pic'],
					usertype=request.POST['usertype'],
					)
				msg="User Signup Are Successsfully"
				return render(request,'login.html',{'msg':msg})
			else:
				msg="Password & Confirm Password Does Not MAtched"
				return render(request,'signup.html',{'msg':msg})
	else:		
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				if user.usertype=="buyer":
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['lname']=user.lname
					request.session['profile_pic']=user.profile_pic.url
					wishlists=Wishlist.objects.filter(user=user)
					request.session['wishlist_count']=len(wishlists)
					carts=Cart.objects.filter(user=user,payment_status=False)
					request.session['cart_count']=len(carts)
					return redirect('index')
				else:
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['lname']=user.lname
					request.session['profile_pic']=user.profile_pic.url
					return redirect('seller-index')
			else:
				msg="Incorrect Password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="Email Not Registered"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['lname']
		del request.session['profile_pic']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def change_password(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		if user.password==request.POST['oldpassword']:
			if request.POST['newpassword']==request.POST['cnewpassword']:
				user.password=request.POST['newpassword']
				user.save()
				msg="Change Password Successsfully"
				return redirect('logout')
			else:
				msg="New Password & Confirm New password Does Not Matched"
				if user.usertype=="buyer":
					return render(request,'change-password.html',{'msg':msg})
				else:
					return render(request,'seller-change-password.html',{'msg':msg})

		else:
			msg="Password & Old password Does Not Matched"
			if user.usertype=="buyer":
				return render(request,'change-password.html',{'msg':msg})
			else:
				return render(request,'seller-change-password.html',{'msg':msg})
	else:
		if user.usertype=="buyer":
			return render(request,'change-password.html')
		else:
			return render(request,'seller-change-password.html')

def edit_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		msg="Edit Profile Successsfully"
		request.session['fname']=user.fname
		request.session['lname']=user.lname
		request.session['profile_pic']=user.profile_pic.url 
		if user.usertype=="buyer":
			return render(request,'edit-profile.html',{'user':user,'msg':msg})
		else:
			return render(request,'seller-edit-profile.html',{'user':user,'msg':msg})
	else:	
		if user.usertype=="buyer":
			return render(request,'edit-profile.html',{'user':user})
		else:
			return render(request,'seller-edit-profile.html',{'user':user})

def seller_add_product(request):
	seller=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		Product.objects.create(
			seller=seller,
			product_category=request.POST['product_category'],
			product_name=request.POST['product_name'],
			product_price=request.POST['product_price'],
			product_desc=request.POST['product_desc'],
			product_image=request.FILES['product_image'],
			)
		msg="Product Added Successsfully"
		return render(request,'seller-add-product.html',{'msg':msg})
	else:	
		return render(request,'seller-add-product.html')

def seller_view_product(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,'seller-view-product.html',{'products':products})

def seller_product_details(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'seller-product-details.html',{'product':product})

def seller_edit_product(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_category=request.POST['product_category']
		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_desc=request.POST['product_desc']
		try:
			product.product_image=request.FILES['product_image']
		except:
			pass
		product.save()
		msg="Product Update Successsfully"
		return render(request,'seller-edit-product.html',{'product':product,'msg':msg})
	else:
		return render(request,'seller-edit-product.html',{'product':product})

def seller_delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller-view-product')

def seller_view_laptop(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Laptop")
	return render(request,'seller-view-product.html',{'products':products})

def seller_view_camera(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Camera")
	return render(request,'seller-view-product.html',{'products':products})

def seller_view_accessories(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Accessories")
	return render(request,'seller-view-product.html',{'products':products})

def seller_order(request):
	myorder = []
	seller=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(payment_status=True)
	for i in carts:
		if i.product.seller == seller:
			myorder.append(i)
	return render(request,'seller-order.html',{'myorder':myorder})

def laptop(request):
	products=Product.objects.filter(product_category="Laptop")
	msg="Laptop"
	return render(request,'store.html',{'products':products,'msg':msg})

def camera(request):
	products=Product.objects.filter(product_category="Camera")
	msg="Camera"
	return render(request,'store.html',{'products':products,'msg':msg})

def accessories(request):
	products=Product.objects.filter(product_category="Accessories")
	msg="Accessories"
	return render(request,'store.html',{'products':products,'msg':msg})

def store(request):
	products=Product.objects.all()
	return render(request,'store.html',{'products':products})

def shop(request):
	#seller=User.objects.get(email=request.session['email'])
	products=Product.objects.all()
	return render(request,'shop.html',{'products':products})


def product_details(request,pk):
	wishlist_flag=False
	cart_flag=False
	product=Product.objects.get(pk=pk)
	path=request.get_full_path()
	
	try:
		user=User.objects.get(email=request.session['email'])
		Wishlist.objects.get(user=user,product=product)
		wishlist_flag=True
	except:
		pass
	try:
		user=User.objects.get(email=request.session['email'])
		Cart.objects.get(user=user,product=product,payment_status=False)
		cart_flag=True
	except:
		pass
	return render(request,'product-details.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(user=user,product=product)
	return redirect('wishlist')

def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	return render(request,'wishlist.html',{'wishlists':wishlists})

def remove_from_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('wishlist')

def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(
		user=user,
		product=product,
		product_price=product.product_price,
		product_qty=1,
		total_price=product.product_price
		)

	return redirect('cart')

def cart(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)
	for i in carts:
		net_price=net_price+i.total_price
	return render(request,'cart.html',{'carts':carts,'net_price':net_price})

def remove_from_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(user=user,product=product,payment_status=False)
	cart.delete()
	return redirect('cart')

def change_qty(request):
	pk=int(request.POST['pk'])
	cart=Cart.objects.get(pk=pk)
	product_qty=int(request.POST['product_qty'])
	cart.product_qty=product_qty
	cart.total_price=cart.product_price*product_qty
	cart.save()

	return redirect('cart')

def myorder(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=True)
	return render(request,'myorder.html',{'carts':carts})