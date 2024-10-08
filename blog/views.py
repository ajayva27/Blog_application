# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Post,UserProfile
from .serializers import PostSerializer
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib.auth import get_user_model, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated



User = get_user_model()

# API ViewSet for Posts
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.get_serializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# User signup view
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'blog/signup.html', {
                'username': username,
                'email': email,
            })

        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email address already exists.')
            return render(request, 'blog/signup.html', {
                'username': username,
                'email': email,
            })

        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'blog/signup.html', {
                'username': username,
                'email': email,
            })

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully! You can log in now.')
        return redirect('login')  

    return render(request, 'blog/signup.html')


# Custom login view
class CustomLoginView(LoginView):
    template_name = 'blog/login.html'  
    success_url = reverse_lazy('post_list')  

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')  
        return super().form_invalid(form)


# Logout view
def logout_view(request):
    logout(request)
    return redirect('post_list')


# List of posts
def post_list(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=query).order_by('-created_at') if query else Post.objects.all().order_by('-created_at')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'query': query})


# user profile 
@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    posts = Post.objects.filter(author=request.user)  # Display the user's posts
    profile_picture = profile.profile_picture.url if profile.profile_picture else '{% static "image/default_pro_pic.jpeg" %}'
    return render(request, 'blog/user_profile.html', {'posts': posts, 'profile_picture': profile_picture})


# edit profile 
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user_profile = user.userprofile

        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        
        if request.FILES.get('profile_picture'):
            user_profile.profile_picture = request.FILES.get('profile_picture')
        elif request.POST.get('remove_picture') == 'True':
            user_profile.profile_picture = None  
        
        user.save()
        user_profile.save()
        
        return redirect('user_profile')  

    return render(request, 'blog/edit_profile.html', {'user': request.user})


# Create a new post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


# Edit existing post
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


# View a specific post
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/view_post.html', {'post': post})
