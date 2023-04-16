from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .filters import *
from .forms import OrderForm,CreateCustomerForm,CreateUserForm
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib import messages

# Create your views here.
#creation register view function
@unauthenticated_user
def registerpage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			#add into customer group during account creation
			group = Group.objects.get(name='customer') 
			user.groups.add(group)
			# OneToOne relationship
			Customer.objects.create(
				user=user,name=user.username,
			)
			#showing flash messages form account creation
			messages.success(request,'Account was created for '+ username) #show flash message with username
			return redirect('login')
	context = {'form':form}
	return render(request,'crm_app/register.html',context)

#creating loginpage view function
@unauthenticated_user
def loginpage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.info(request,'Username or Password is Incorrect')
			# return render(request,'crm_app/login.html',context)
	context = {}
	return render(request,'crm_app/login.html',context)

#creating logout view function
def logoutpage(request):
	logout(request)
	return redirect('login')


#creating homepage view function for admin only
@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders,'customers':customers,'total_customers':total_customers,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'crm_app/dashboard.html',context)

#creating userpage view function
@allowed_users(allowed_roles=['customer'])
def userpage(request):
	orders = request.user.customer.order_set.all()
	print(orders)
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	context = {'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
	return render(request,'crm_app/user.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def settings(request):
	customer = request.user.customer
	form = CreateCustomerForm(instance=customer)
	if request.method == 'POST':
		form = CreateCustomerForm(request.POST,request.FILES,instance=customer)
		if form.is_valid():
			form.save
	context = {'form':form}
	return render(request,'crm_app/account_settings.html',context)

#creating products page view function
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'crm_app/products.html',context)

#creating customer page view function
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	order_count = orders.count()
	myfilter = OrderFilter(request.GET,queryset=orders)
	orders = myfilter.qs
	context = {'customer':customer,'orders':orders,'order_count':order_count,'myfilter':myfilter}
	return render(request, 'crm_app/customer.html',context)

#creating CreatOrder page view function
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request,'crm_app/orderform.html',context)

#creating UpdateOrder page view function
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request,'crm_app/orderform.html',context)

#creating deleteOrder page view function
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {'item':order}
	return render(request,'crm_app/delete.html',context)

#creating cratecustomer page view function
@login_required(login_url='login')
def createCustomer(request):
	form = CreateCustomerForm()
	if request.method == 'POST':
		form = CreateCustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request,'crm_app/customerform.html',context)

#creating update customer page view function
@login_required(login_url='login')
def updateCustomer(request,pk):
	customer = Customer.objects.get(id=pk)
	form = CreateCustomerForm(instance=customer)
	if request.method == 'POST':
		form = CreateCustomerForm(request.POST,instance=customer)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request,'crm_app/customerform.html',context)

#creating deleting cutomer view function
@login_required(login_url='login')
def deleteCustomer(request,pk):
	customer = Customer.objects.get(id=pk)
	if request.method == 'POST':
		customer.delete()
		return redirect('/')
	context = {'item':customer}
	return render(request,'crm_app/delete.html',context)