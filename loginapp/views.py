from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

def index(request):
    context = {
        'all_users' : User.objects.all(),
    }
    return render (request, 'home.html', context)

def show_reg_page(request):
    context = {
        'all_users' : User.objects.all(),
    }
    return render (request, 'registration.html', context)

def show_login_page(request):
    context = {
        'all_users' : User.objects.all(),
    }
    return render (request, 'login.html', context)

def create_user (request): 
    if request.method == 'POST':    
        errors = User.objects.RegistrationValidator(request.POST)
        if len(errors) >0: 
            for k,v in errors.items():
                messages.error(request, v)
                
            return redirect('/show_reg_page')
        
        else: 
            hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            role = request.POST['role']
            
            new_user = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = hashedpw, role = role)
            new_user_id = new_user.id
            request.session['user'] = new_user_id
            
            if role == 'Wedding Planner':
                return redirect('/show_planner_profile')
            else:
                return redirect('/show_cust_profile')
    
    else:
        return redirect ( '/')
    
    
def show_planner_profile(request):
    log_user = User.objects.get(id = request.session['user'])
    planners = Planner.objects.all()
    context = {
        'all_users' : User.objects.all(),
        'user': log_user,
        'planners': planners
    }
    return render (request, 'planner_profile.html', context)

def show_cust_profile(request):
    log_user = User.objects.get(id = request.session['user'])
    context = {
        'all_users' : User.objects.all(),
        'user': log_user
    }
    return render (request, 'cust_profile.html', context)
    
def user_login(request): 
    if request.method == 'POST':
        errors = User.objects.LoginValidator(request.POST)
        if len(errors) >0: 
            for k,v in errors.items():
                messages.error(request, v)
                
            return redirect ('/')
        
        else:
            user_log = User.objects.get(email = request.POST['email'])
            request.session['user'] = user_log.id
            user_id = user_log.id
            return redirect (f'/show_user_info/{user_id}')
        
    else:
        return redirect('/')
    
def create_planner_profile(request):
    log_user = User.objects.get(id = request.session['user'])
    destination = request.POST['destination']
    months = request.POST['months']
    budgets = request.POST['budgets']
    new_planner = Planner.objects.create(planner = log_user, destination = destination, months = months, budget = budgets)
    new_planner_id = new_planner.id
    user_id = log_user.id
    return redirect (f'/show_user_info/{user_id}')

def create_customer_profile(request):
    log_user = User.objects.get(id = request.session['user'])
    destination = request.POST['cust_destination']
    months = request.POST['cust_months']
    budgets = request.POST['cust_budgets']
    activities = request.POST['cust_activities']
    new_customer = Customer.objects.create(customer = log_user, destination = destination, months = months, budget = budgets, activity = activities)
    new_customer_id = new_customer.id
    user_id = log_user.id
    return redirect (f'/show_user_info/{user_id}')

def leave_message(request): 
    log_user = User.objects.get(id = request.session['user'])
    posted_by_user = User.objects.get(id = request.POST['posted_by'])
    posted_for_user = User.objects.get(id = request.POST['posted_for'])
    user_id = posted_for_user.id
    message = request.POST['message']
    
    new_message = Message.objects.create(message = message, posted_by = posted_by_user, posted_for = posted_for_user)
    
    return redirect (f'/show_user_info/{user_id}')

def leave_comment(request): 
    log_user = User.objects.get(id = request.session['user'])
    posted_by_user = User.objects.get(id = request.POST['posted_by'])
    message = Message.objects.get(id = request.POST['message_id'])
    user_id = posted_by_user.id
    comment = request.POST['comment']
    
    new_comment = Comment.objects.create(comment = comment, posted_by = posted_by_user, message = message)
    return redirect (f'/show_user_info/{user_id}')
    
def show_user_info(request, user_id):
    logged_user = User.objects.get(id = request.session['user'])
    info_user = User.objects.get(id = user_id)
    all_messages = logged_user.posted_for.all()
    planners = Planner.objects.all()
    users = User.objects.all()
    customers = Customer.objects.all()
    all_messages = Message.objects.all()
    
    context = {
        'user': logged_user,
        'all_messages': all_messages,
        'planners': planners,
        'users': users,
        'customers':customers
    }
    return render (request, 'user_info.html', context)

def show_profile_page(request):
    logged_user = User.objects.get(id = request.session['user'])
    if logged_user.role == "Wedding Planner":
        user = Planner.objects.get (planner = logged_user)
    else:
        user = Customer.objects.get(customer = logged_user)
    context = {
        'log_user': logged_user,
        'user':user
    }
    return render (request, 'profile_page.html', context)

def delete(request, user_id):
    log_user = User.objects.get(id = request.session['user'])
    log_user_id = log_user.id
    delete_user = User.objects.get(id = user_id)
    delete_user.delete()
    return redirect (f'/show_user_info/{log_user_id}')


def logout(request):
    del request.session['user']
    return redirect('/')