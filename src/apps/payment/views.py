from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import PaymentRequestSerializer
from django.conf import settings


import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentRequestView(generics.GenericAPIView):

    serializer_class = PaymentRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        intent = stripe.PaymentIntent.create(
            amount=459,
            currency='aud',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
        )
        
        return Response(
            {
                'clientSecret': intent['client_secret'],
                # [DEV]: For demo purposes only, you should avoid exposing the PaymentIntent ID in the client-side code.
                'dpmCheckerLink': 'https://dashboard.stripe.com/settings/payment_methods/review?transaction_id={}'.format(intent['id']),
            }, 
            status=status.HTTP_200_OK
        )


# class InitiatePaymentView(generics.GenericAPIView):
#     serializer_class = InitiatePaymentSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         response = serializer.validated_data.get('response')

#         return Response(response,status=status.HTTP_200_OK)
    
# class VerifyPaymentView(generics.GenericAPIView):
#     serializer_class = VerifyPaymentSerializer

#     def get(self, request, *args, **kwargs):
#         pidx = request.GET.get('pidx')
#         serializer = self.get_serializer(data={'pidx': pidx})
#         serializer.is_valid(raise_exception=True)
        
#         response = serializer.validated_data.get('response')

#         return Response(response,status=status.HTTP_200_OK)