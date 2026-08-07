from django.contrib.auth import logout
from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from sabzsocial import settings
from taggit.models import Tag
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.postgres.search import SearchVector , SearchQuery , SearchRank , TrigramSimilarity
# Create your views here.

@login_required
def profile(request):
    user = get_object_or_404(User , pk= request.user.id)
    return render(request , 'social/profile.html' , {'user' : user})

def log_out(request):
    logout(request)
    return redirect('social:login')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST , request.FILES)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request , 'registration/register_done.html' , {'user':user})
    else :
        form = RegisterForm()
    return render(request, 'forms/register.html' , {'form':form})

@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST , request.FILES , instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('social:profile')
    else:
        user_form = EditUserForm(instance=request.user)
    context = {
        'user_form':user_form,
    }
    return render(request , 'registration/edit_user.html' , context)

def ticket(request):
    sent = False
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"{cd['name']}\n{cd['email']}\n\n{cd['message']}"
            send_mail(cd['subject'],message,'samazolfkhani12@gmail.com',['samazolfkhani12@gmail.com'] , fail_silently=False)
            sent = True
    else:
        form = TicketForm()
    return render(request,'forms/ticket.html',{'form': form,'sent': sent})

def post_list(request , tag_slug = None):
    posts = Post.objects.all()
    tag = None
    if tag_slug :
        tag = get_object_or_404(Tag , slug = tag_slug)
        posts = Post.objects.filter(tags__in = [tag])
    paginator = Paginator(posts , 2)
    page_number = request.GET.get('page' , 1)
    posts = paginator.page(page_number)
    context = {
        'posts' : posts ,
        'tag' : tag
    }
    return render(request , "social/list.html" , context)


@login_required()
def create_post (request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST , request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            form.save_m2m()
            image1 = form.cleaned_data['image1']
            image2 = form.cleaned_data['image2']
            if image1 :
                Image.objects.create(image_file = image1 , post=post)
            if image2 :
                Image.objects.create(image_file = image2 , post=post)
            return redirect('social:profile')
    else :
        form = CreatePostForm()
    return render(request, 'forms/create_post.html' , {'form':form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_tags_ids = post.tags.values_list("id", flat=True)
    images = list(post.images.all())
    similar_posts = (
        Post.objects.filter(tags__in=post_tags_ids)
        .exclude(id=post.id)
        .annotate(same_tags=Count("tags"))
        .order_by("-same_tags", "-created")[:2])
    comments = post.comments.all()   
    paginator = Paginator(comments ,4)    
    page_number = request.GET.get("page")
    comments = paginator.get_page(page_number)
    form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "similar_posts": similar_posts,
        "images" : images
    }

    return render(request, "social/detail.html", context )

@login_required
def post_comment(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    return redirect("social:post_detail", post_id=post.id)

@login_required()
def edit_post (request , post_id):
    post = get_object_or_404(Post , id = post_id)
    if request.method == 'POST':
        form = CreatePostForm(request.POST , request.FILES , instance = post)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            form.save_m2m()
            image1 = form.cleaned_data['image1']
            image2 = form.cleaned_data['image2']
            if image1 :
                Image.objects.create(image_file = image1 , post=post)
            if image2 :
                Image.objects.create(image_file = image2 , post=post)
            return redirect('social:post_detail' , post_id = post.id)
    else :
        form = CreatePostForm(instance = post)
    return render(request, 'forms/create_post.html' , {'form':form})

@login_required
def delete_post(request , post_id):
    post = get_object_or_404(Post , id = post_id)
    if request.method == "POST" :
        post.delete()
        return redirect('social:profile')
    return render(request ,'forms/delete_post.html' , {'post' : post})

def search(request):
    query = None
    posts = []
    if 'query' in request.GET :
        form = SearchForm(data = request.GET) 
        if form.is_valid(): 
            query = form.cleaned_data['query']
            search_query = SearchQuery(query)
            search_vetcor = SearchVector('description' , weight="A") + SearchVector('tags__name' , weight = "B")
            posts = Post.objects.annotate(rank = SearchRank(search_vetcor , search_query) , 
                                  similarity = TrigramSimilarity('description' , query) + TrigramSimilarity('tags__name' , query)).\
            filter(Q(rank__gte = 0.1) | Q(similarity__gt = 0.3)).order_by('-rank' , '-similarity')
    context = {
        'query' : query ,
        'posts' : posts
    }
    return render(request , 'social/search.html' , context)

