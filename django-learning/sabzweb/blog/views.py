from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponse ,Http404
from .models import *
from .forms import TicketForm, CommentForm, CreatePostForm , SearchForm
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.views.generic import ListView , DetailView
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q


# Create your views here.

def index(request):
    return render(request, 'blog/index.html')

# def post_list(request):
#     posts = Post.published.all()
#     paginator = Paginator(posts , 2)
#     page_number = request.GET.get('page' , 1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     context = {
#         'posts' : posts,
#     }
#     return render(request , 'blog/list.html' , context)

class PostListView(ListView):
    queryset = Post.published.all()
    template_name = 'blog/list.html'
    paginate_by = 2
    context_object_name = 'posts'

def post_detail(request , id):
    post = get_object_or_404(Post , id = id , status = Post.Status.PUBLISHED)
    comments = post.comments.filter(active = True)
    form = CommentForm()
    context = {
        'post' : post,
        'comments' : comments,
        'form' : form,
    }
    return render(request , 'blog/detail.html' , context)

# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'


def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(message = cd['message'] , name = cd['name'] , email = cd['email'] , phone = cd['phone'] ,
                                                             subject = cd['subject'])
            return redirect('blog:index')
    else:
        form = TicketForm()
        return render(request, 'forms/ticket.html', {'form':form})



@require_POST
def post_comment(request , id):
    post = get_object_or_404(Post , id = id , status = Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit = False)
        comment.post = post
        comment.save()
    context = {
        'post':post ,
        'comment':comment,
        'form':form,
    }
    return render(request , 'forms/comment.html' , context)


def post_search(request):
    query = None
    result = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            result1 = Post.published.annotate(similarity=TrigramSimilarity('title' , query)).\
                filter(similarity__gte = 0.2).order_by('-similarity')
            result2 = Post.published.annotate(similarity = TrigramSimilarity('description' , query)).\
                filter(similarity__gte = 0.2).order_by('-similarity')
            result = result1 | result2
    context = {
        'query':query,
        'result':result,
    }
    return render(request , 'blog/search.html' , context )


def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    context = {
        'posts':posts,
        'user':user,
    }
    return render(request , 'blog/profile.html' , context)

def create_post (request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST , request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'] , post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'] , post=post)
            return redirect('blog:profile')
    else :
        form = CreatePostForm()
    return render(request, 'forms/create_post.html' , {'form':form})