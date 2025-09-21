from django.shortcuts import render,redirect ,get_object_or_404 
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Product , Customer , Cart
from . form import CustomRegisterForm 
from . form import CustomerProfileForm
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.
def home(request):
    """Render the home page."""
    return render(request, 'app/home.html')


def about(request):
    """Render the about page."""
    return render(request, 'app/about.html')


def contact(request):
    """Render the contact page."""
    return render(request, 'app/contact.html')


class CategoryView(View):
    """Display products filtered by category."""

    def get(self, request, val):
        products = Product.objects.filter(category=val)
        titles = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", {"products": products, "titles": titles})


class CategoryTitle(View):
    """Display products filtered by title within a category."""

    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html", {"products": product, "titles": title})


class ProductDetail(View):
    """Display details of a specific product."""

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/product.html", locals())


class CustomerRegistrationView(View):
    """Handle customer registration."""

    def get(self, request):
        form = CustomRegisterForm()
        return render(request, 'app/registration.html', locals())

    def post(self, request):
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/registration.html', locals())


class ProfileView(View):
    """Manage customer profile."""

    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            self._extracted_from_post_4(request, form)
        else:
            messages.warning(request, 'Invalid Data Input')
        return render(request, 'app/profile.html', locals())

    # TODO Rename this here and in `post`
    def _extracted_from_post_4(self, request, form):
        user = request.user
        name = form.cleaned_data['name']
        locality = form.cleaned_data['locality']
        city = form.cleaned_data['city']
        mobile = form.cleaned_data['mobile']
        state = form.cleaned_data['state']
        zipcode = form.cleaned_data['zipcode']

        reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
        reg.save()
        messages.success(request, 'Congratulations! Profile saved Successfully')


def address(request):
    """Display customer addresses."""
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add})


class UpdateAddress(View):

    def get(self, request, pk):
        addd = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=addd)
        return render(request, 'app/updateaddress.html', {'form': form})

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST,)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()

            messages.success(request, 'Congratulations! Profile saved Successfully')
        else:
            messages.warning(request, 'Invalid Data Input')
        return redirect('address')


def add_to_cart(request):
    """Add a product to the user's cart."""
    user = request.user
    product_id = request.GET.get('prod_id')

    if not product_id:
        messages.error(request, "No product selected to add to cart.")
        return redirect('home')

    try:
        product_id = int(product_id)
    except ValueError:
        messages.error(request, "Invalid product id.")
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)

    Cart(user=user, product=product).save()
    return redirect('showcart')


def show_cart(request):
    """Display the user's cart with total amounts."""
    user = request.user
    carts = Cart.objects.filter(user=user)
    amount = 0
    for p in carts:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    total_amount = amount + 40

    return render(request, 'app/addtocart.html', {'carts': carts, 'amount': amount, 'total_amount': total_amount})

class Checkout(LoginRequiredMixin, View):
    def get(self,request):
        user = request.user
        addresses = Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        context = {
            'addresses': addresses,
            'cart_items': cart_items,
            'totalamount': totalamount,
        }
        return render(request, "app/checkout.html", context)
     



def calculate_cart_totals(user):
    cart = Cart.objects.filter(user=user)
    amount = sum(p.quantity * p.product.discounted_price for p in cart)
    total_amount = amount + 40 if cart else 0
    return amount, total_amount


@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            c.quantity += 1
            c.save()
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)

        amount, total_amount = calculate_cart_totals(request.user)

        return JsonResponse({
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total_amount,
        })


@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            if c.quantity > 1:
                c.quantity -= 1
                c.save()
            else:
                c.delete()
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)

        amount, total_amount = calculate_cart_totals(request.user)

        return JsonResponse({
            'quantity': c.quantity if c.id else 0,
            'amount': amount,
            'totalamount': total_amount,
        })


@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            c.delete()  
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)

        amount, total_amount = calculate_cart_totals(request.user)

        return JsonResponse({
            'amount': amount,
            'totalamount': total_amount,
        })

# def payment_done(request):
#     if request.method == "POST":
#         # yahan aapka payment processing ka code
#         # Example: address select karna, order create karna, cart khali karna
#         return render(request, "paymentdone.html")
#     else:
#         return HttpResponse("Method Not Allowed", status=405)



def payment_done(request):
    """Render the contact page."""
    return render(request, 'app/paymentdone.html')

