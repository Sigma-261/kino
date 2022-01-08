from django.conf.urls.static import static
from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('', views.index, name = 'home'),
    path('movies/', views.ModelView.as_view(), name = 'movies'),
    path('<slug:slug>/', views.ModelDetailView.as_view(), name = 'movie_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name = 'add_review'),
    path('actor/<str:slug>/', views.ActorViews.as_view(), name = 'actor_detail'),
    path('schedule', views.schedule, name = 'schedule'),
    path('promotions', views.promotions, name = 'promotions'),
    path('about-us', views.about, name = 'about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)