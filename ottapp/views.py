from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth import login,logout
from . models import OTT_user,Subscription,Movies
# from django.contrib.auth.hashers import check_password
import datetime
# from django.db import connection
# Create your views here.
def home(request):
    return render(request, 'landing.html')

def signup(request):
    if request.method == 'POST':
        F_name = request.POST.get('F_name')      
        L_name = request.POST.get('L_name')      
        email = request.POST.get('email')      
        password = request.POST.get('password')
        user = OTT_user.objects.filter(email = email)
        if user.exists():
            messages.error(request, 'This email is already registered. Please sign in.')
            return redirect('signup')
        try:
            user = OTT_user.objects.create(
                first_name = F_name,
                last_name = L_name,
                email = email,
                username = F_name
            )
            user.set_password(password)
            user.save()
            login(request,user)
            messages.success(request,'Signup successfull! Welcome')
            return redirect('subscription')
        except Exception as e:
            messages.error(request, 'An error occurred during signup. Please try again.')

    return render(request, 'signup.html')


def subscription(request):
    if request.method == 'POST':
        plan_name = request.POST.get('plan')
        date  = datetime.date.today()
        next_month = date.month + 1 if date.month < 12 else 1
        date = datetime.date(date.year + 1 if next_month == 1 else date.year, next_month, date.day)
        try:
            user = request.user
            plan = Subscription.objects.create(
            plan_name = plan_name,
            exp_date = date,
            U_id = user
                )
            plan.save()
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, 'Failed to create subscription. Please try again.')
    return render(request, 'subscription.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')      
        password = request.POST.get('password') 
        c_user = OTT_user.objects.filter(email = email)
        try:
            if c_user.exists():
                c_user = OTT_user.objects.get(email = email)
                if c_user.check_password(password):
                    login(request,c_user)
                    id = request.user.U_id
                    c_user = Subscription.objects.filter(U_id = id)
                    if c_user.exists():
                        return redirect('dashboard')
                    else:
                        return redirect('subscription')
                else:
                    messages.error(request,'Invalid password credentials')
                    # return  redirect('signin')
            else:
                messages.error(request, 'Invalid email. Please try again.')
        except Exception as e:
            messages.error(request, 'An error occurred during signin. Please try again.')
            
    return render(request,'signin.html')


def dashboard(request):
    try:
        movies = Movies.objects.order_by('?')[:5]
        c_user = request.user
        sub = Subscription.objects.filter(U_id = c_user)
        return render(request, 'dashboard.html',{'movies':movies,'user':c_user,'subs':sub})
    except Exception as e:
        messages.error(request, 'Failed to load the dashboard. Please try again.') 

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('')
    

def search(request):
    query = request.GET.get('query', '') # Get the search query from the frontend
    try:
        if query:
            movies = Movies.objects.filter(M_name__icontains=query)  # Filter movies by title
        else:
            movies = Movies.objects.all() 
        context = {
            'movies': movies,
            'query': query,
        }
        return render(request, 'search.html',context)
    except Exception as e:
        messages.error(request, 'An error occurred during search. Please try again.')
        return redirect('search')


def movies(request):
    try:
        movies = Movies.objects.all()
        return render(request, 'movies.html',{'movies':movies})
    except Exception as e:
        messages.error(request, 'Failed to load the movies. Please try again.')


def tv_shows(request):
    try:
        movies = Movies.objects.raw("SELECT * from ottapp_movies ORDER BY RANDOM() LIMIT 3")
        return render(request, 'tv_shows.html',{'movies':movies})
    except Exception as e:
        messages.error(request,'Failed to load the TV Shows. Please try again.')


def recently_watched(request):
    try:
        movies = Movies.objects.raw("SELECT * from ottapp_movies ORDER BY RANDOM() LIMIT 2")
        return render(request, 'recently_watched.html',{'movies':movies})
    except Exception as e:
        messages.error(request,'Failed to load the recently watched. Please try again.')


def more(request):
    try:
        movies = Movies.objects.all()
        return render(request, 'more.html',{'movies':movies})
    except Exception as e:
        messages.error(request,'Failed to load more. Please try again.')
