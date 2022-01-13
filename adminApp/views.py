from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .forms import CakeImageForm
from . models import *


class Login(View):
    def get(self, request):
        try:
            template = 'login.html'
            return render(request, template)
        except Exception as e:
            messages.add_message(request, messages.WARNING, 'Something went wrong. ' + str(e))
            return HttpResponseRedirect(redirect_to='/login')

    def post(self, request):
        try:
            user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                user_role = user.role.id
                user_id = user.id
                name = f'{user.first_name} {user.last_name}'
                request.session['user_role'] = user_role
                request.session['user_id'] = user_id
                request.session['name'] = name
                if user_role == 1:
                    redirect_url = '/dashboard'
                else:
                    redirect_url = '/'
                messages.add_message(request, messages.SUCCESS, 'Welcome to cake shop')
            else:
                redirect_url = '/login'
                messages.add_message(request, messages.WARNING, 'Wrong credentials provided')
            return HttpResponseRedirect(redirect_to=redirect_url)
        except Exception as e:
            messages.add_message(request, messages.WARNING, 'Something went wrong. ' + str(e))
            return HttpResponseRedirect(redirect_to='/login')

class RegistrationView(View):
    def get(self, request):
        try:
            template = 'register.html'
            roles = UserRole.objects.all()
            return render(request, template, context={
                'roles': roles
            })
        except Exception as e:
            return HttpResponse(str(e))

    def post(self, request):
        try:
            user = User.objects.create(
                role_id=request.POST['role_id'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                password=make_password(request.POST['password'])
            )
            user.save()
            if (request.POST['role_id'] == 1):# seller
                message = 'Registration success. Please login to continue..'
                redirect_url = '/login'
            else:
                message = 'Registration success'
                redirect_url = '/login'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(redirect_to=redirect_url)
        except Exception as e:
            messages.add_message(request, messages.WARNING, 'Something went wrong. ' + str(e))
            return HttpResponseRedirect(redirect_to='/registration')

class LogoutView(View):
    def get(self, request):
        try:
            request.session.flush()
            messages.add_message(request, messages.SUCCESS, 'Successfully logged out')
            return HttpResponseRedirect(redirect_to='/login')
        except Exception as e:
            messages.add_message(request, messages.WARNING, 'Something went wrong. ' + str(e))
            return HttpResponseRedirect(redirect_to='/dashboard')

class Dashboard(View):
    def get(self, request):
        try:
            template = 'dashboard.html'
            return render(request, template)
        except Exception as e:
            return HttpResponse(str(e))

class MyShopView(View):
    def get(self, request):
        try:
            template = 'shops.html'
            shop = Shop.objects.all()
            return render(request, template, context={
                'shops': shop
            })
        except Exception as e:
            return HttpResponse(str(e))

class DeleteShopView(View):
    def get(self, request, shop_id):
        try:
            delete = Shop.objects.filter(pk=shop_id).delete()
            if (delete):
                message = "shop deleted successfully"
            else:
                message = "Failed to delete shop"
            return HttpResponseRedirect(redirect_to='/my-shop')
        except Exception as e:
            return HttpResponse(str(e))

class EditShopView(View):
    def get(self, request, shop_id):
        try:
            shop = Shop.objects.get(pk=shop_id)
            template = 'add_shop.html'
            heading = 'Edit Shop'
            return render(request, template, context={
                'heading': heading,
                'shop': shop,
                'shop_id': shop.id
            })
        except Exception as e:
            return HttpResponse(str(e))

class CakeView(View):
    def get(self, request):
        try:
            template = 'cakes.html'
            cakes = Cake.objects.all()
            return render(request, template, context={
                'cakes': cakes
            })
        except Exception as e:
            return HttpResponse(str(e))

class EditCakeView(View):
    def get(self, request, cake_id):
        try:
            cake = Cake.objects.get(pk=cake_id)
            template = 'add_cake.html'
            heading = 'Edit Cake'
            return render(request, template, context={
                'heading': heading,
                'cake': cake,
                'cake_id': cake.id
            })
        except Exception as e:
            return HttpResponse(str(e))

class BookingView(View):
    def get(self, request):
        try:
            template = 'bookings.html'
            bookings = Booking.objects.all()
            return render(request, template, context={
                'bookings': bookings
            })
        except Exception as e:
            return HttpResponse(str(e))

class AddCakeView(View):
    def get(self, request):
        try:
            template = 'add_cake.html'
            categories = Category.objects.all()
            weights = CakeWeight.objects.all()
            shops = Shop.objects.all()
            heading = 'Add Cake'
            return render(request, template, context={
                'categories': categories,
                'shops': shops,
                'weights': weights,
                'heading': heading,
                'cake_id': -1
            })
        except Exception as e:
            return HttpResponse(str(e))

    def post(self, request):
        try:
            if (int(request.POST['cake_id']) > 0):
                cake = Cake.objects.get(pk=request.POST['cake_id'])
                cake.name = request.POST['name']
                cake.price = request.POST['price']
                cake.category_id = request.POST['category']
                cake.weight_id = request.POST['weight']
                cake.shop_id = request.POST['shop']
                cake.description = request.POST['description']
            else:
                cake = Cake.objects.create(
                    name=request.POST['name'],
                    price=request.POST['price'],
                    category_id=request.POST['category'],
                    weight_id=request.POST['weight'],
                    shop_id=request.POST['shop'],
                    description=request.POST['description']
                )
            cake.save()
            return HttpResponseRedirect(redirect_to='/cakes')
        except Exception as e:
            return HttpResponse(str(e))

class AddFlavourView(View):
    def get(self, request):
        try:
            template = 'add_flavour.html'
            cake = Cake.objects.all()
            return render(request, template, context={
                'cakes': cake
            })
        except Exception as e:
            return HttpResponse(str(e))

    def post(self, request):
        try:
            cake_id = request.POST['cake_id']
            cake = CakeFlavour.objects.create(
                name=request.POST['flavour'],
                cake_id=cake_id,
            )
            cake.save()
            return HttpResponseRedirect(redirect_to='/cake-details/'+cake_id)
        except Exception as e:
            messages.add_message(request, messages.SUCCESS, 'Something went wrong. '+str(e))
            return HttpResponseRedirect(redirect_to='/registration')

class AddShopView(View):
    def get(self, request):
        try:
            template = 'add_shop.html'
            heading = 'Add Shop'
            return render(request, template, context={
                'heading': heading,
                'shop_id': -1
            })
        except Exception as e:
            return HttpResponse(str(e))

    def post(self, request):
        try:
            if (int(request.POST['shop_id']) > 0):
                shop = Shop.objects.get(pk=request.POST['shop_id'])
                shop.user_id = request.session['user_id']
                shop.name = request.POST['name']
                shop.address = request.POST['address']
                shop.location = request.POST['location']
                shop.pincode = request.POST['pincode']
                message = "Shop updated successfully"
            else:
                shop = Shop.objects.create(
                    user_id=request.session['user_id'],
                    name=request.POST['name'],
                    address=request.POST['address'],
                    location=request.POST['location'],
                    pincode=request.POST['pincode']
                )
                message = "Shop created successfully"
            shop.save()
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(redirect_to='/my-shops')
        except Exception as e:
            messages.add_message(request, messages.WARNING, 'Something went wrong. '+str(e))
            return HttpResponseRedirect(redirect_to='/add-shop')


class AddImageView(View):
    def get(self, request):
        try:
            template = 'add_image.html'
            cake = Cake.objects.all()
            return render(request, template, context={
                'cakes': cake
            })
        except Exception as e:
            return HttpResponse(str(e))

    def post(self, request):
        try:
            cake_id = request.POST['cake_id']
            post_data = {
                'cake': cake_id
            }
            form = CakeImageForm(post_data, request.FILES)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Cake image added successfully')
            else:
                messages.add_message(request, messages.WARNING, 'Image upload failed. Try again later. '+str(form))
            return HttpResponseRedirect(redirect_to='/cake-details/' + cake_id)
        except Exception as e:
            messages.add_message(request, messages.WARNING, 'Something went wrong. Error: ' + str(e))
            return HttpResponseRedirect(redirect_to='/add-image')



class DeleteCakeView(View):
    def get(self, request, cake_id):
        try:
            delete_cake = Cake.objects.filter(pk=cake_id).delete()
            if (delete_cake):
                message = "Cake deleted successfully"
            else:
                message = "Failed to delete cake"
            return HttpResponseRedirect(redirect_to='/cakes')
        except Exception as e:
            return HttpResponse(str(e))

class CakeDetailsView(View):
    def get(self, request, cake_id):
        try:
            template = 'cake_details.html'
            cake = Cake.objects.get(pk=cake_id)
            cake_flavour = CakeFlavour.objects.filter(cake=cake_id)
            cake_images = CakeImage.objects.filter(cake=cake_id)
            return render(request, template, context={
                'cake': cake,
                'cake_flavour': cake_flavour,
                'cake_images': cake_images,
            })
        except Exception as e:
            return HttpResponse(str(e))