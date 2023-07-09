from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from account.views import RegisterViewSet

account_router = DefaultRouter()
account_router.register('register', RegisterViewSet, basename='account')
urlpatterns = [
                  path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
              ] + account_router.urls
