from django.urls import path
from .views import PaymentRequestView

urlpatterns = [
    path('initiate/', PaymentRequestView.as_view(), name='initiate-payment-api'),
    # path('verify/', VerifyPaymentView.as_view(), name='verify-payment-api'),
]