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
    path('dashboard/',views.dashboard, name='dashboard'),
    path('search/',views.search, name='search'),
    path('movies/',views.movies, name='movies'),
    path('tv_shows/',views.tv_shows, name='tv_shows'),
    path('recently_watched/',views.recently_watched, name='recently_watched'),
    path('more/',views.more, name='more'),
    path('logout/',views.logout_view, name='logout'),
]

if  settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


