from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm,CreateCustomerForm
# Create your views here.


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders,'customers':customers,'total_customers':total_customers,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'crm_app/dashboard.html',context)

def products(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'crm_app/products.html',context)

def customer(request,pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	order_count = orders.count()
	context = {'customer':customer,'orders':orders,'order_count':order_count}
	return render(request, 'crm_app/customer.html',context)

def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request,'crm_app/orderform.html',context)

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

def deleteOrder(request,pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {'item':order}
	return render(request,'crm_app/delete.html',context)

def createCustomer(request):
	form = CreateCustomerForm()
	if request.method == 'POST':
		form = CreateCustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request,'crm_app/customerform.html',context)


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

def deleteCustomer(request,pk):
	customer = Customer.objects.get(id=pk)
	if request.method == 'POST':
		customer.delete()
		return redirect('/')
	context = {'item':customer}
	return render(request,'crm_app/delete.html',context)