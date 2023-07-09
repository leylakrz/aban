from rest_framework.routers import DefaultRouter

from transaction.views import TransactionViewSet

transaction_router = DefaultRouter()
transaction_router.register('', TransactionViewSet, basename='transaction')
urlpatterns = [

              ] + transaction_router.urls
