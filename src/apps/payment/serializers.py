from rest_framework import serializers,exceptions

class PaymentRequestSerializer(serializers.Serializer):
    group_id = serializers.UUIDField()


# import json
# from src.apps.announcement.models import Announcement
# from src.apps.auth.models import User
# import os
# import requests

# class InitiatePaymentSerializer(serializers.Serializer):
#     user_id = serializers.CharField(max_length=255,required=True,allow_blank=False)
#     announcement_id = serializers.CharField(max_length=255,required=True,allow_blank=False)
#     return_url = serializers.URLField(required=True)
#     amount = serializers.FloatField(required=True)

#     def validate(self, attrs):
#         announcement_id = attrs.get('announcement_id',None)
#         try:
#             announcement = Announcement.objects.get(id=announcement_id)
#         except announcement.DoesNotExist:
#             raise exceptions.APIException('Announcement does not exist')

#         user_id = attrs.get('user_id',None)
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             raise exceptions.APIException('User does not exist')

#         purchase_order_id = str(announcement.id)
#         purchase_order_name = announcement.title
#         amount = attrs.get('amount',None)
#         return_url = attrs.get('return_url',None)

#         url = f'{os.environ.get("KHALTI_BASE_URL")}epayment/initiate/'

#         payload = json.dumps({
#             "return_url": return_url,
#             "website_url": "http://127.0.0.1:8000",
#             "amount": amount,
#             "purchase_order_id": purchase_order_id,
#             "purchase_order_name": purchase_order_name,
#             "customer_info":{
#                 "name":f'{user.first_name} {user.last_name}',
#                 "email":"test@khalti.com",
#                 'phone':"9800000001"
#             }
#         })

#         headers = {
#             'Authorization': f"key {os.environ.get('KHALTI_SECRET_KEY')}",
#             'Content-Type': 'application/json'
#         }
        
#         response = requests.request("POST",url,headers=headers, data=payload)

#         res = json.loads(response.text)
        
#         announcement.pidx = res.get('pidx')
#         announcement.save()
        
#         attrs['response'] = res
#         return attrs
    

# class VerifyPaymentSerializer(serializers.Serializer):

#     pidx = serializers.CharField(max_length=255, required=True, allow_blank=False)

#     def validate(self, attrs):
#         pidx = attrs.get('pidx',None)

#         url = f'{os.environ.get("KHALTI_BASE_URL")}epayment/lookup/'

#         payload = json.dumps({
#             "pidx": pidx,
#         })

#         headers = {
#             'Authorization': f"key {os.environ.get('KHALTI_SECRET_KEY')}",
#             'Content-Type': 'application/json'
#         }

#         response = requests.request("POST",url,headers=headers,data=payload)

#         res = json.loads(response.text)

#         attrs['response'] = res

#         if res.get('status')!= 'Completed':
#             raise exceptions.APIException(res.get('status'))
        
#         try:
#             announcement = Announcement.objects.get(pidx=pidx)
#         except announcement.DoesNotExist:
#             raise exceptions.APIException('Payment for this announcement, not found')
        
#         announcement.paid_for_email = True
#         announcement.paid_amount = f"{res.get('total_amount')}-{res.get('fee')}"
#         announcement.save()
        
#         return attrs