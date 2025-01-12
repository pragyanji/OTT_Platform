from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth import login,logout,update_session_auth_hash
from . models import OTT_user,Subscription,Movies
from django.core.files.storage import FileSystemStorage
import datetime

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
    return render(request, 'subscription_base.html')

def new_subscription(request):
    plans = [
        {'name': 'Basic', 'price': 200, 'duration': 30},
        {'name': 'Standard', 'price': 1100, 'duration': 180},
        {'name': 'Premium', 'price': 2000, 'duration': 365},
    ]
    user = request.user
    if user.subscription_set.exists():
        messages.error(request, 'You already have a subscription!!')
        return redirect('dashboard')
    if request.method == 'POST':
        plan_name = request.POST.get('plan')
        date = datetime.date.today()
        try:
            if plan_name == 'Basic':
                exp_date = date + datetime.timedelta(days=30)
            elif plan_name == 'Standard':
                exp_date = date + datetime.timedelta(days=180)
            else:  # Premium
                exp_date = date + datetime.timedelta(days=365)

            user = request.user
            plan = Subscription.objects.create(
                plan_name=plan_name,
                exp_date=exp_date,
                U_id=user
            )
            plan.save()
            messages.success(request, f'Subscribed to {plan_name} successfully!')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, 'Failed to create subscription. Please try again.')

    return render(request, 'new_subscription.html', {'plans': plans})

def renew_subscription(request):
    try:
        user = request.user
        subscription = Subscription.objects.filter(U_id = user).first()
        if subscription:
            content = {
                'subscription':subscription
            }
        else:
            messages.error(request,"you have not subscribed any plan till now!!")
            return redirect('new_subscription')
        if request.method == 'POST':
            plan_name = request.POST.get('plan')
            date  = datetime.date.today()
            if subscription.exp_date > date:
                date = subscription.exp_date
            if plan_name == 'Basic':
                exp_date = date + datetime.timedelta(days=30)
            elif plan_name == 'Standard':
                exp_date = date + datetime.timedelta(days=180)
            else:  # Premium
                exp_date = date + datetime.timedelta(days=365)

            subscription.plan_name = plan_name
            subscription.exp_date = exp_date
            subscription.save()
            messages.success(request, 'Subscription renewed successfully!')
            return redirect('dashboard')
    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred while managing subscription. Please try again.')    
    return render(request,'renew_subscription.html',content)

def upgrade_downgrade_subscription(request):
    try:
        user = request.user
        subscription = Subscription.objects.filter(U_id = user).first()
        if not subscription:
            messages.error(request,"you have not subscribed any plan till now!!")
            return redirect('new_subscription')
            
        plans = [
            {'name': 'Basic', 'price': 200, 'duration': 30},
            {'name': 'Standard', 'price': 1100, 'duration': 180},
            {'name': 'Premium', 'price': 2000, 'duration': 365},
            ]
        if request.method == 'POST':
            plan_name = request.POST.get('plan')
            date  = datetime.date.today()
            selected_plan = next((plan for plan in plans if plan['name'] == plan_name), None)
            # Determine the current plan index and the selected plan index
            current_plan_index = next((index for index, plan in enumerate(plans) if plan['name'] == subscription.plan_name), None)
            selected_plan_index = next((index for index, plan in enumerate(plans) if plan['name'] == selected_plan['name']), None)
            if selected_plan_index > current_plan_index:
                # Upgrade logic
                messages.success(request, f"You have chosen to upgrade to {selected_plan['name']} plan. The upgrade will be applied after your current plan expires.")
            elif selected_plan_index < current_plan_index:
                # Downgrade logic
                messages.success(request, f"You have chosen to downgrade to {selected_plan['name']} plan. The downgrade will be applied after your current plan expires.")
            else:
                # Same plan
                messages.info(request, "You are already on the selected plan.")
                return redirect('upgrade_downgrade_subscription')
            # Store the selected plan in session data for later processing
            request.session['next_plan'] = {
                'name': selected_plan['name'],
                'price': selected_plan['price'],
                'duration': selected_plan['duration'],
            }
            return redirect('dashboard')
    except Exception as e:
            messages.error(request, 'An error occurred while managing subscription. Please try again.')
    return render(request,'upgrade_downgrade_subscription.html',{'plans': plans})
         
# def apply_next_plan(subscription, session_data):
#     if subscription.end_date <= date.today():
#         next_plan = session_data.get('next_plan')
#         if next_plan:
#             subscription.plan_name = next_plan['name']
#             subscription.end_date = date.today() + datetime.timedelta(days=next_plan['duration'])
#             subscription.save()
#             # Clear the next plan details from the session
#             session_data.pop('next_plan', None)   

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
                    messages.success(request,'Login Successfull!!')
                    id = request.user.U_id
                    c_user = Subscription.objects.filter(U_id = id)
                    if c_user.exists():
                        return redirect('dashboard')
                    else:
                        return redirect('subscription')
                else:
                    messages.error(request,'Invalid password credentials')
            else:
                messages.error(request, 'Invalid email. Please try again.')
                
        except Exception as e:
            messages.error(request, 'An error occurred during signin. Please try again.')
            
    return render(request,'signin.html')


def dashboard(request):
    try:
        movies = Movies.objects.order_by('?')[:5]
        user = request.user
        todays_date  = datetime.date.today()
        sub = Subscription.objects.filter(U_id = user).first()
        if sub and sub.exp_date<todays_date:
            next_plan = request.session.get('next_plan')
            if next_plan:
                sub.plan_name = next_plan['name']
                sub.exp_date = todays_date + datetime.timedelta(days=next_plan['duration'])
                sub.save()
                # Clear the next plan details from the session
                request.session.pop('next_plan', None)
                # Notify the user of the applied plan
                messages.success(request, f"Your subscription has been updated to the {next_plan['name']} plan.")
            else:
                messages.error(request,f"Subscription Expired on {sub.exp_date}")
                return redirect('renew_subscription')
        else:
            if request.method == 'POST':
                email = request.POST.get('email')
                password = request.POST.get('password')
                profile = request.FILES.get('profile')
                if email:
                    user.email = email

                if password:
                    user.set_password(password)
                    update_session_auth_hash(request, user)

                if profile:
                    fs = FileSystemStorage()
                    filename = fs.save(profile.name, profile)
                    user.profile_pic = filename
                user.save()
                messages.success(request, 'Profile updated successfully!!')
            context = {'movies':movies,
                       'user':user,
                       'subscription':sub}
            return render(request, 'dashboard.html',context) 
    except Exception as e:
        messages.error(request, f'Failed to load the dashboard. Please try again.')
        return redirect('dashboard')
    
  
    
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
        movies = Movies.objects.filter(content_type = 'Movie')
        return render(request, 'movies.html',{'movies':movies})
    except Exception as e:
        messages.error(request, 'Failed to load the movies. Please try again.')


def tv_shows(request):
    try:
        TV_Show = Movies.objects.filter(content_type = 'TV Show')
        return render(request, 'tv_shows.html',{'movies':TV_Show})
    except Exception as e:
        messages.error(request,'Failed to load the TV Shows. Please try again.')


def recently_added(request):
    try:
        movies = Movies.objects.all().order_by('-added_on')
        return render(request, 'recently_added.html',{'movies':movies})
    except Exception as e:
        messages.error(request,'Failed to load the recently added. Please try again.')


def more(request):
    try:
        movies = Movies.objects.all()
        return render(request, 'more.html',{'movies':movies})
    except Exception as e:
        messages.error(request,'Failed to load more. Please try again.')

def help(request):
    try:
        return render(request, 'help.html')
    except Exception as e:
        messages.error(request,'Failed to load help. Please try again.')

def terms_and_condition(request):
    return render(request, 'terms_and_condition.html')


def feedback(request):
    if request.method == 'POST':
        try:
            feedback = request.POST.get('message', '')
            messages.success(request, "Thank you for your feedback!")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, 'Failed to submit feedback. Please try again.')
    return render(request, 'feedback.html')