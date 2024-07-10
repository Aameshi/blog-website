from django.shortcuts import render

# Create your views here.
from .models import Post
from django.utils import timezone

def post_list(request):
    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

from django.shortcuts import get_object_or_404

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

from.forms import PostForm
from django.shortcuts import redirect

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            authenticate(username=username, password=password)
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form':form})

from .forms import ForgotPasswordForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user:
                # Send email
                subject = "Login Details"
                message = render_to_string('blog/forgot_password_mail.html', {'user': user})
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Your login details have been sent on your mail.')
            else:
                messages.error(request, 'Email not registered.')
                return redirect('forgot_password')
            # return redirect('login')
    else:
        form = ForgotPasswordForm()
    return render(request, 'blog/forgot_password.html', {'form': form})