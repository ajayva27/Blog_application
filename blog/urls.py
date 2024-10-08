from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

from .views import PostViewSet, signup_view, CustomLoginView, logout_view, create_post, edit_post, post_list, user_profile, edit_profile, view_post

# Setting up the router for REST API
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    path('api/', include(router.urls)),  
    path('api/posts/', PostViewSet.as_view({'post': 'create'}), name='post-list'),
    path('api/posts/<int:pk>/', PostViewSet.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'}), name='post-detail'),

    
    path('post/new/', create_post, name='create_post'),  # Create post
    path('post/edit/<int:pk>/', edit_post, name='edit_post'),  # Edit post
    path('post/<int:post_id>/', view_post, name='view_post'),  # View individual post

   
    path('', post_list, name='post_list'),  # List all posts
    path('login/', CustomLoginView.as_view(), name='login'),  # User login
    path('logout/', logout_view, name='logout'),  # User logout
    path('signup/', signup_view, name='signup'),  # User signup
    path('profile/', user_profile, name='user_profile'),  # User profile
    path('profile/edit/', edit_profile, name='edit_profile'),  # Edit user profile
]
