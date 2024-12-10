from rest_framework import generics,status,permissions
from rest_framework.response import Response
from .serializers import PaymentRequestSerializer, GroupPaymentAcceptSerializer
from django.conf import settings
from decimal import Decimal
from datetime import datetime, timedelta

from src.apps.payment.models import GroupPayment, PaymentStatus
from src.apps.group.models import AnnouncementGroup

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentRequestView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = PaymentRequestSerializer

    def post(self, request, *args, **kwargs):

        intent = stripe.PaymentIntent.create(
            amount=459,
            currency='aud',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
        )

        # data = request.data.copy()  # Create a mutable copy of request.data
        # data['payment_intent'] = intent['id']
        # serializer = self.get_serializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        try:
            group = AnnouncementGroup.objects.get(group_id=request.data.get('group',None))
        except AnnouncementGroup.DoesNotExist:
            return Response({'error': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        payment = GroupPayment.objects.create(
            group=group,
            user=request.user,
            payment_intent=intent['id'],
        )

        return Response(
            {
                'clientSecret': intent['client_secret'],
                # [DEV]: For demo purposes only, you should avoid exposing the PaymentIntent ID in the client-side code.
                'dpmCheckerLink': 'https://dashboard.stripe.com/settings/payment_methods/review?transaction_id={}'.format(intent['id']),
            }, 
            status=status.HTTP_200_OK
        )


class GroupPaymentAcceptView(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = GroupPaymentAcceptSerializer

    def post(self, request, *args, **kwargs):
        payment_intent_id = request.data.get('payment_intent')

        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        except stripe.error.InvalidRequestError as e: # type: ignore
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if payment_intent.status == 'succeeded':
            try:
                payment = GroupPayment.objects.get(payment_intent=payment_intent_id)
                payment.payment_status = PaymentStatus.SUCCESS
                payment.amount = Decimal(payment_intent.amount/100)
                payment.currency = payment_intent.currency
                payment.recurring_date = datetime.now() + timedelta(days=365)
                payment.save()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': payment_intent.status}, status=status.HTTP_200_OK)

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