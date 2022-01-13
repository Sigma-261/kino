import datetime

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.db.models import Q
from .models import Promotions, Movie, Category, Actor, Session
from .forms import ReviewForm


def index(request):
    return render(request, 'main/index.html')


class ModelView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'main/movies.html'
    context_object_name = 'movies'

    def get_context_data(self, *args, **kwargs):
        print(args, kwargs)
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

class SessionViews(DetailView):
    model = Session

    template_name = "main/session.html"
    slug_field = "url"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class ScheduleView(ListView):
    model = Session
    template_name = 'main/schedule.html'
    context_object_name = 'sessions'
    queryset = Session.objects.filter(date__gt=datetime.date.today())
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class Search(ListView):
    template_name = 'main/search_result.html'
    model = Movie
    context_object_name = 'movies'

    def get_queryset(self):
        query = self.request.GET.get('q')
        movies = Movie.objects.filter(
            Q(title__icontains=query) | Q(category__url__icontains=query)
        )
        return movies
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        return context
    '''def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"), category__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context'''

def schedule(request):
    return render(request, 'main/schedule.html')

def promotions(request):
    promotions = Promotions.objects.all()
    return render(request, 'main/promotions.html', {'promotions':promotions})

def about(request):
    return render(request, 'main/about.html')



