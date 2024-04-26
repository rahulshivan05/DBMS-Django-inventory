from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Product, Transaction, Supplier
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TransactionForm, ProductForm, SupplierForm


def home(request):
    suppliers = Supplier.objects.all()
    products = Product.objects.all()
    context = {
        'suppliers': suppliers,
        'products': products,
    }
    return render(request, 'app/welcome-page.html', context)


def about(request):
    context = {}
    return render(request, 'app/about.html', context)


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'app/product_list.html'


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'app/product_detail.html'


def create_transaction(request, transaction_type, product_id, quantity):
    product = get_object_or_404(Product, pk=product_id)
    if transaction_type == 'in':
        product.quantity_in_stock += quantity
    elif transaction_type == 'out':
        product.quantity_in_stock -= quantity
    else:
        # Handle invalid transaction type here
        pass
    product.save()
    transaction = Transaction.objects.create(
        transaction_type=transaction_type,
        product=product,
        quantity=quantity,
        user=request.user,  # Assumes user is authenticated
    )
    # Handle transaction success/failure here
    pass


@login_required
def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-timestamp')
    return render(request, 'app/transactions.html', {'transactions': transactions})


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction created.')
            return redirect('transaction')
    else:
        form = TransactionForm()
    return render(request, 'app/transaction_create.html', {'form': form})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = product
            transaction.save()
            if transaction.transaction_type == 'sale':
                product.quantity_in_stock -= transaction.quantity
                product.save()
            if transaction.transaction_type == 'purchase' or transaction.transaction_type == 'return':
                product.quantity_in_stock += transaction.quantity
                product.save()
            return redirect('inventory:product_detail', pk=product_id)
    else:
        form = TransactionForm()
    return render(request, 'app/product_detail2.html', {'product': product, 'form': form})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm()
    return render(request, 'app/add_product.html', {'form': form})


def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'app/add_supplier.html', {'form': form})


def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'app/supplier_list.html', {'suppliers': suppliers})


def supplier_detail(request, supplier_id):
    supplier_details = get_object_or_404(Supplier, pk=supplier_id)
    context = {
        'suppliers': supplier_details
    }
    return render(request, 'app/supplier_detail.html', context)
