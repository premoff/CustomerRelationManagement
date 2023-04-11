from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .filters import *
from .forms import OrderForm,CreateCustomerForm,CreateUserForm

#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.

def registerpage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request,'Account was created for '+ user) #show flash message with username
				return redirect('loginpage')
		context = {'form':form}
		return render(request,'crm_app/register.html',context)


def loginpage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
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


def logoutpage(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders,'customers':customers,'total_customers':total_customers,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'crm_app/dashboard.html',context)

@login_required(login_url='login')
def products(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'crm_app/products.html',context)

@login_required(login_url='login')
def customer(request,pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	order_count = orders.count()
	myfilter = OrderFilter(request.GET,queryset=orders)
	orders = myfilter.qs
	context = {'customer':customer,'orders':orders,'order_count':order_count,'myfilter':myfilter}
	return render(request, 'crm_app/customer.html',context)

@login_required(login_url='login')
def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request,'crm_app/orderform.html',context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def deleteOrder(request,pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {'item':order}
	return render(request,'crm_app/delete.html',context)

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

@login_required(login_url='login')
def deleteCustomer(request,pk):
	customer = Customer.objects.get(id=pk)
	if request.method == 'POST':
		customer.delete()
		return redirect('/')
	context = {'item':customer}
	return render(request,'crm_app/delete.html',context)