from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .models import Article, Category, Product
from pfa import views





def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
   
# def home(request): 
#     #  # Récupérer les produits que vous souhaitez afficher sur la page d'accueil
#     # products = Product.objects.filter(available=True)  # Vous pouvez ajouter des filtres ici, par exemple [:6] pour limiter à 6 produits

#     # context = {
#     #     'products': products
#     # # }
#     #  return render(request, 'index.html')
#     # return render(request, 'home.html', context)
    
#      return render(request, 'home.html')

def home(request):
    categories = Category.objects.prefetch_related('products').all()
    trending_products = Product.objects.all().order_by('-id')[:5]
    articles = Article.objects.all()

    context = {
        'trending_products': trending_products,
        'categories':categories,
    }
    return render(request, 'home.html', context)
    
 



def about(request):
    articles = Article.objects.all()
    return render(request, 'about.html', {'articles': articles})

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})







class ShopView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'shop.html', {'products': products})





def collection_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'collection.html', {'category': category, 'products': products})


# views.py

def cart_view(request):
    cart = request.session.get('cart', {})
    return render(request, 'cart.html', {'cart': cart})



# views.py

def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Logique pour ajouter le produit au panier de l'utilisateur
    # Par exemple, en utilisant des sessions
    cart = request.session.get('cart', {})
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product.name,
            'price': product.price,
            'quantity': 1,
            'image': product.image.url,
        }
    request.session['cart'] = cart
    return redirect('cart')


   
  
def signin(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile') #profile
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
  
def profile(request): 
    return render(request, 'profile.html')
   
def signout(request):
    logout(request)
    return redirect('/')






