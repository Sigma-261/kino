from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Promotions, Movie, Category, Actor
from .forms import ReviewForm

def index(request):
    return render(request, 'main/index.html')
class ModelView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'main/movies.html'
    context_object_name = 'movies'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        return context

class ModelDetailView(DetailView):
    model = Movie
    slug_field = "url"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        return context
class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie=movie
            form.save()
        return redirect(movie.get_absolute_url())

class ActorViews(DetailView):
    model = Actor
    template_name = "main/actor.html"
    slug_field = "name"

class ScheduleView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'main/schedule.html'
    context_object_name = 'movies'

def schedule(request):
    return render(request, 'main/schedule.html')

def promotions(request):
    promotions = Promotions.objects.all()
    return render(request, 'main/promotions.html', {'promotions':promotions})

def about(request):
    return render(request, 'main/about.html')



