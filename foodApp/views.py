from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from .forms import CustomAuthenticationForm, CustomerRegistrationForm, DeliveryInfoForm, FoodForm, AddFoodForm
from .models import Food, RestaurantOwner, Category, Cart, DeliveryInfo, Order


# Create your views here.

def index(request):
    foods = Food.objects.all()[:6]
    authors = RestaurantOwner.objects.all()[:6]
    categories = Category.objects.all()[:6]
    context = {"foods": foods, "authors": authors, "categories": categories}
    return render(request, "index.html", context)


def search(request):
    authors = RestaurantOwner.objects.all()[:5]
    categories = Category.objects.all()[:5]
    search_term = request.GET.get('search_term')
    foods = Food.objects.filter(title__icontains=search_term)[:6]
    context = {"foods": foods, "authors": authors, "categories": categories, "search_term": search_term}
    return render(request, 'index.html', context)


def details(request, food_id=None):
    food = get_object_or_404(Food, id=food_id)
    isInShoppingCart = False
    context = {
        'food': food,
        'isInShoppingCart': isInShoppingCart,
    }
    return render(request, 'details.html', context)


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # Redirect to the login page after successful registration
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def handle_form_submission(request, food_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_to_cart':
            food = Food.objects.get(id=food_id)
            quantity = int(request.POST.get('quantity', 1))
            cart_item, created = Cart.objects.get_or_create(user=request.user, food=food)
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            return redirect('/cart')


def cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_price = 0
    for item in cart_items:
        item.total_price = item.quantity * item.food.price
        total_price += item.total_price

    return render(request, 'cart.html', {'cart_items': cart_items, "total": total_price})




def place_order(request):
    user = request.user
    delivery_info = None

    try:
        delivery_info = DeliveryInfo.objects.get(user=user)
        initial_data = {
            'name': delivery_info.name,
            'surname': delivery_info.surname,
            'address': delivery_info.address,
            'city': delivery_info.city,
            'country': delivery_info.country,
            'phone': delivery_info.phone,
        }
    except DeliveryInfo.DoesNotExist:
        initial_data = {}

    if request.method == 'POST':
        form = DeliveryInfoForm(request.POST)
        if form.is_valid():
            if delivery_info:
                delivery_info.name = form.cleaned_data['name']
                delivery_info.surname = form.cleaned_data['surname']
                delivery_info.address = form.cleaned_data['address']
                delivery_info.city = form.cleaned_data['city']
                delivery_info.country = form.cleaned_data['country']
                delivery_info.phone = form.cleaned_data['phone']
                delivery_info.save()
            else:
                delivery_info = DeliveryInfo.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    surname=form.cleaned_data['surname'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    country=form.cleaned_data['country'],
                    phone=form.cleaned_data['phone']
                )

            cart_items = Cart.objects.filter(user=user)
            total_price = 0
            for item in cart_items:
                item.total_price = item.quantity * item.food.price
                total_price += item.total_price

            order = Order.objects.create(
                user=user,
                delivery_info=delivery_info,
                total_price=total_price
            )
            return redirect('/confirmed')
    else:
        form = DeliveryInfoForm(initial=initial_data)

    return render(request, 'deliveryinfo.html', {'form': form})


def confirmed(request):
    Cart.objects.filter(user=request.user).delete()
    return render(request, 'confirm.html')


def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart')


def filter_foods(request):
    selected_author = request.GET.get('author')
    selected_category = request.GET.get('category')
    authors = RestaurantOwner.objects.all()[:6]
    categories = Category.objects.all()[:6]

    foods = Food.objects.all()

    if selected_author:
        foods = foods.filter(owner=selected_author)

    if selected_category:
        foods = foods.filter(category=selected_category)

    context = {"foods": foods, "authors": authors, "categories": categories}
    return render(request, 'index.html', context)


def edit_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            if 'image' not in request.FILES:  # No new photo uploaded
                form.fields['image'].required = False
            form.save()
            # Redirect to the book details page or any other appropriate URL
            return redirect('food_details', food_id=food_id)
        else:
            print(form.errors)
    else:

        form = FoodForm(instance=food)

    return redirect('food_details', food_id=food_id)


def add_food(request):
    if request.method == 'POST':
        form = AddFoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the book details page or any other appropriate URL
            return redirect('food_details', food_id=form.instance.id)
    else:
        form = AddFoodForm()

    return render(request, 'addFood.html', {'form': form})


def delete_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    food.delete()
    # Redirect to the book list page or any other appropriate URL
    return redirect('/')


def contact(request):
    return render(request, "contact.html")

