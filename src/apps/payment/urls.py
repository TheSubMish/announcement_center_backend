from django.urls import path
from .views import PaymentRequestView, GroupPaymentAcceptView

urlpatterns = [
    path('initiate/', PaymentRequestView.as_view(), name='initiate-payment-api'),
    path('complete/', GroupPaymentAcceptView.as_view(), name='complete-payment-api'),
]