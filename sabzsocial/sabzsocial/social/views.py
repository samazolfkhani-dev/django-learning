from django.contrib.auth import logout
from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse , JsonResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from sabzsocial import settings
from taggit.models import Tag
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.postgres.search import SearchVector , SearchQuery , SearchRank , TrigramSimilarity
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.contrib import messages
# Create your views here.

@login_required
def profile(request):
    user = User.objects.prefetch_related('followers').get(id=request.user.id)
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
            messages.success(request , 'Sent Successfuly!')
    else:
        form = TicketForm()
    return render(request,'forms/ticket.html',{'form': form,'sent': sent})

def post_list(request , tag_slug = None):
    posts = Post.objects.select_related('author').order_by('-total_likes' , '-id')
    tag = None
    if tag_slug :
        tag = get_object_or_404(Tag , slug = tag_slug)
        posts = posts.filter(tags__in = [tag]).distinct()
    page = request.GET.get('page')
    paginator = Paginator(posts , 2)
    try :
        posts = paginator.page(page)
    except PageNotAnInteger :
        posts = paginator.page(1)
    except EmptyPage:
        posts = []
    if request.GET.get('ajax') :
        return render(request , 'social/list_ajax.html' , {'posts' : posts})
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

@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None :
        post = get_object_or_404(Post , id = post_id)
        user = request.user
        if user in post.likes.all() :
            post.likes.remove(user)
            liked = False
        else :
            post.likes.add(user)
            liked = True
        post_likes_count = post.likes.count()
        response_data = {
            'liked' : liked ,
            'likes_count' : post_likes_count 
        }
    else :
        response_data={
            'error' : 'Invalid Post Id!'
        }
    return JsonResponse(response_data)

@login_required
@require_POST
def saved_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = get_object_or_404(Post , id = post_id)
        user = request.user

        if user in post.saved_by.all():
            post.saved_by.remove(user)
            saved = False
        else :
            post.saved_by.add(user)
            saved = True

        return JsonResponse({'saved' : saved})
    return JsonResponse({'error' : 'Invalid Post Id!'})

@login_required
def user_list(request):
    users = User.objects.filter(is_active = True)
    return render(request , 'user/user_list.html' , {'users' : users}) 

@login_required
def user_detail(request , username) :
    user = get_object_or_404(User , username = username , is_active = True)
    return render(request , 'user/user_detail.html' , {'user' : user})

@login_required
@require_POST
def follow(request):
    user_id = request.POST.get('id')
    if user_id :
        try :
            user = get_object_or_404(User , id = user_id)
            if request.user in user.followers.all() :
                Contact.objects.filter(user_from = request.user , user_to = user).delete()
                follow = False
            else :
                Contact.objects.get_or_create(user_from = request.user , user_to = user)
                follow = True
            followers = user.followers.count()
            followings = user.following.count()
            return JsonResponse({'follow' : follow , 'followers' : followers , 'followings' : followings})
        except User.DoesNotExist :
            return JsonResponse({'error' : 'User Does Not Exist!'})
    return JsonResponse({'error' : 'Invalid Request!'})


