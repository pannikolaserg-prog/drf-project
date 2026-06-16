from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .apps import UsersConfig
from .views import UserCreateView

app_name = UsersConfig.name

urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]
