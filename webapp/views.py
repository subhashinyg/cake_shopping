from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.http import HttpResponse
from adminApp.models import Shop, Cake, User

from .models import Cart, Order


class Home(View):
    def get(self, request):
        try:
            scheme = request.is_secure() and "https" or "http"
            host = request.get_host()
            base_url = f'{scheme}://{host}/'
            template = 'index.html'
            shops = Shop.objects.all()
            cakes = Cake.objects.all()
            cart = []
            if ('user_id' in request.session and request.session['user_id']):
                cart = Cart.objects.filter(user=request.session['user_id'])

            return render(request, template, context={
                'shops': shops,
                'cakes': cakes,
                'base_url': base_url,
                'cart': cart,
            })
        except Exception as e:
            return HttpResponse(str(e))

class ShopCakes(View):
    def get(self, request, shop_id):
        try:
            scheme = request.is_secure() and "https" or "http"
            host = request.get_host()
            base_url = f'{scheme}://{host}/'
            cart = []
            if (request.session['user_id']):
                cart = Cart.objects.filter(user=request.session['user_id'])

            template = 'shop_cakes.html'
            shop = Shop.objects.get(pk=shop_id)
            shop_cakes = Cake.objects.filter(shop=shop_id)
            return render(request, template, context={
                'shop': shop,
                'shop_cakes': shop_cakes,
                'base_url': base_url,
                'cart': cart,
            })
        except Exception as e:
            return HttpResponse(str(e))

class AboutView(View):
    def get(self, request):
        try:
            template = 'about.html'
            return render(request, template)
        except:
            pass

class ProductView(View):
    def get(self, request):
        try:
            scheme = request.is_secure() and "https" or "http"
            host = request.get_host()
            base_url = f'{scheme}://{host}/'
            cart = []
            if (request.session['user_id']):
                cart = Cart.objects.filter(user=request.session['user_id'])
            template = 'product.html'
            cakes = Cake.objects.all()
            return render(request, template, context={
                'cakes': cakes,
                'base_url': base_url,
                'cart': cart
            })
        except:
            pass
class CartView(View):
    def get(self, request):
        try:
            template = 'cart.html'
            scheme = request.is_secure() and "https" or "http"
            host = request.get_host()
            base_url = f'{scheme}://{host}/'
            cart = []
            sub_total = 0
            total_price = 0
            delivery_charge = 0
            discount = 0
            if (request.session['user_id'] and Cart.objects.filter(user=request.session['user_id']).exists()):
                cart = Cart.objects.filter(user=request.session['user_id'])
                cart_total = cart.aggregate(Sum('total_price'))
                sub_total = cart_total['total_price__sum']
                delivery_charge = settings.DELIVERY_CHARGE
                discount = settings.DISCOUNT
                total_price = sub_total + delivery_charge
                discount_price = (settings.DISCOUNT * total_price) / 100
                total_price -= round(discount_price)
            return render(request, template, context={
                'base_url': base_url,
                'cart': cart,
                'sub_total': sub_total,
                'delivery_charge': delivery_charge,
                'discount': discount,
                'total_price': total_price,
            })
        except Exception as e:
            return HttpResponse(str(e))

class CartAddView(View):
    def get(self, request, cake_id):
        try:
            user_id = request.session['user_id']
            cake = Cake.objects.get(pk=cake_id)
            if (Cart.objects.filter(user=user_id, cake=cake_id).exists()):
                cart = Cart.objects.get(user=user_id, cake=cake_id)
                qty = cart.qty + 1
                total_price = cake.price * qty
                update = Cart.objects.filter(user=user_id, cake=cake_id).update(qty=qty, total_price=total_price)
                if (update):
                    message = 'Cart updated successfully'
                else:
                    message = 'Cart updated successfully'
            else:
                cart = Cart.objects.create(
                    user_id=user_id,
                    cake_id=cake_id,
                    total_price=cake.price
                )
                cart.save()
                message = 'Product added to cart successfully'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(redirect_to='/cart')
        except Exception as e:
            messages.add_message(request, messages.WARNING, 'Something went wrong. Error: '+str(e))
            return HttpResponseRedirect(redirect_to='/')

class RemoveCartView(View):
    def get(self, request, cart_id):
        try:
            delete = Cart.objects.filter(pk=cart_id).delete()
            return HttpResponseRedirect(redirect_to='/cart')
        except Exception as e:
            messages.add_message(request, messages.WARNING, 'Something went wrong. Error: '+str(e))
            return HttpResponseRedirect(redirect_to='/cart')

class CartUpdateView(View):
    def post(self, request):
        try:
            qty = request.POST.get('qty')
            total_price = request.POST.get('total_price')
            cart_id = request.POST.get('cart_id')
            update = Cart.objects.filter(id=cart_id).update(qty=qty, total_price=total_price)
            if (update):
                return HttpResponse(True)
            else:
                return HttpResponse(False)
        except Exception as e:
            return HttpResponse(str(e))

class CheckoutView(View):
    def post(self, request):
        try:
            template = 'checkout.html'
            user_id = request.session['user_id']
            user = User.objects.get(pk=user_id)
            sub_total = request.POST['sub_total']
            total_price = request.POST['total_price']
            return render(request, template, context={
                'user': user,
                'sub_total': sub_total,
                'total_price': total_price,
                'delivery_charge': settings.DELIVERY_CHARGE,
                'discount': settings.DISCOUNT
            })
        except Exception as e:
            return HttpResponse(str(e))

class PlaceOrderView(View):
    def post(self, request):
        try:
            # with transaction.atomic:
            user_id = request.session['user_id']
            user = User.objects.get(pk=user_id)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.address1 = request.POST['address1']
            user.address2 = request.POST['address2']
            user.city = request.POST['city']
            user.pincode = request.POST['pincode']
            user.phone = request.POST['phone']
            user.email = request.POST['email']
            user.save()

            import string
            import random
            rand_order_id = ''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k=6))

            order = Order.objects.create(
                user_id=user_id,
                sub_total=request.POST['sub_total'],
                delivery_charge=settings.DELIVERY_CHARGE,
                discount=settings.DISCOUNT,
                order_total=request.POST['total_price'],
                order_id=rand_order_id,
            )
            order.save()
            # order_id = order.pk

            Cart.objects.filter(user_id=user_id).delete()
            return HttpResponseRedirect(redirect_to='/cart')

        except Exception as e:
            return HttpResponse(str(e))