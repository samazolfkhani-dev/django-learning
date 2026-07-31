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
        form = RegisterForm(request.POST)
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
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('social:profile')
    else :
        form = CreatePostForm()
    return render(request, 'forms/create_post.html' , {'form':form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_tags_ids = post.tags.values_list("id", flat=True)
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
        else :
            print(form.errors)
    return redirect("social:post_detail", post_id=post.id)