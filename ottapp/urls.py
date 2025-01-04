from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name=''),
    path('home/',views.dashboard, name='home'),
    path('signin/',views.signin, name='signin'),
    path('signup/',views.signup, name='signup'),
    path('subscription/',views.subscription, name='subscription'),
    path('new_subscription/',views.new_subscription, name='new_subscription'),
    path('renew_subscription/',views.renew_subscription, name='renew_subscription'),
    path('upgrade_downgrade_subscription/',views.upgrade_downgrade_subscription, name='upgrade_downgrade_subscription'),
    
    path('dashboard/',views.dashboard, name='dashboard'),
    path('search/',views.search, name='search'),
    path('movies/',views.movies, name='movies'),
    path('tv_shows/',views.tv_shows, name='tv_shows'),
    path('recently_added/',views.recently_added, name='recently_added'),
    path('more/',views.more, name='more'),
    path('logout/',views.logout_view, name='logout'),
    path('help/',views.help, name='help'),
    path('feedback/',views.feedback, name='feedback'),
]

if  settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


