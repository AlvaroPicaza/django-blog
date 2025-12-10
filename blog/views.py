from gc import get_objects

from django.contrib.contenttypes.views import shortcut
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView, CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin



posts = [
    {
        'author': 'PapayaAncestral',
        'title': 'Blog post 1',
        'content': 'Post de prueba con Django',
        'date_posted': '21 de noviembre, 2025',
        'hour_posted': '16:50'
    },
    {
        'author': 'FedericoPP',
        'title': 'Blog post 2',
        'content': 'Un segundo post!',
        'date_posted': '21 de noviembre, 2025',
        'hour_posted': '17:00'
    }
]

"""
Deprecado, usamos PostListView
def home(request):
    context = {
        #Llamamos a todos los posts del modelo Post en bbdd
        'posts': Post.objects.all()
    }
    return render(request,'blog/home.html',context)"""


#Vista del listado
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    #obtenemos el post que estamos actualizando y comprobamos que su autor sea el mismo usuario que esta logeado
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True

        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    #obtenemos el post que estamos actualizando y comprobamos que su autor sea el mismo usuario que esta logeado
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True

        else:
            return False

class UserPostView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        super()
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')


def about(request):
    return render(request,'blog/about.html',{'title':'About'})

def tienda(request):
    return render(request,'blog/tienda.html')