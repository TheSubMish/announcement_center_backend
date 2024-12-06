# from rest_framework import generics,status
# from rest_framework.response import Response
# from .serializers import InitiatePaymentSerializer,VerifyPaymentSerializer


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