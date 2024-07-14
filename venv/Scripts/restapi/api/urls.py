from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from customers.views import CustomUserViewSet
from customers.views import RegisterView,LoginView
from products.views import Todo
from rest_framework_simplejwt.views import TokenRefreshView
from customers.views import ForgotPasswordView, ResetPasswordView

# router = DefaultRouter()
# router.register(r'users', CustomUserViewSet)

urlpatterns = [
    # path('users/', include(router.urls)),
    path('todo/', Todo.as_view(), name='todo'),
    path('todo/<int:pk>/', Todo.as_view(), name='todo-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),

]