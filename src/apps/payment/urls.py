from django.urls import path
from .views import InitiatePaymentView,VerifyPaymentView

urlpatterns = [
    path('initiate/', InitiatePaymentView.as_view(), name='initiate-payment-api'),
    path('verify/', VerifyPaymentView.as_view(), name='verify-payment-api'),
]