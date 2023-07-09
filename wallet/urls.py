from rest_framework.routers import DefaultRouter

from wallet.views import WalletViewSet

wallet_router = DefaultRouter()
wallet_router.register('', WalletViewSet, basename='wallet')
urlpatterns = [

              ] + wallet_router.urls
