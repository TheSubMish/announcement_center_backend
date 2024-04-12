from rest_framework import generics,exceptions,status
from rest_framework.response import Response
from .serializers import (
    CreateAnnouncementGroupSerializer,
    UpdateAnnouncementGroupSerializer,
    AnnouncementGroupSerializer,
    JoinAnnouncementGroupsSerializer
)
from .permissions import (
    CanCreateAnnouncementGroup,
    CanUpdateAnnouncementGroup,
    CanDeleteAnnouncementGroup,
    CanViewAnnouncementGroup,
)
from .models import AnnouncementGroup
from drf_spectacular.utils import extend_schema

class CreateAnnouncementGroupView(generics.CreateAPIView):
    permission_classes = [CanCreateAnnouncementGroup]
    serializer_class = CreateAnnouncementGroupSerializer
    
    @extend_schema(
            responses={
                "application/json": {
                    "example": {
                        "name":"string",
                        "description":"string",
                        "imgae": "image file",
                        "category": "string"
                    }
                }
            }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'msg':'Announcement group created successfully'},status=status.HTTP_201_CREATED)
    

class UpdateAnnouncementGroupView(generics.UpdateAPIView):
    permission_classes = [CanUpdateAnnouncementGroup]
    serializer_class = UpdateAnnouncementGroupSerializer

    def get_queryset(self):
        return AnnouncementGroup.objects.all()
    
    def get_object(self):
        group_id = self.kwargs['pk']
        try:
            announcement_group = AnnouncementGroup.objects.get(group_id=group_id)
        except AnnouncementGroup.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement group does not exist'})
        return announcement_group
    

class DestroyAnnouncementGroupView(generics.DestroyAPIView):
    permission_classes = [CanDeleteAnnouncementGroup]
    serializer_class = AnnouncementGroupSerializer

    def get_queryset(self):
        return AnnouncementGroup.objects.all()

    def get_object(self):
        group_id = self.kwargs['pk']
        try:
            announcement_group = AnnouncementGroup.objects.get(group_id=group_id)
        except AnnouncementGroup.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement group does not exist'})
        return announcement_group
    
class ListAnnouncementGroupView(generics.ListAPIView):
    permission_classes = [CanViewAnnouncementGroup]
    serializer_class = AnnouncementGroupSerializer

    def get_queryset(self):
        return AnnouncementGroup.objects.all()
    

class ListUserCreatedAnnouncementGroupView(generics.ListAPIView):
    permission_classes = [CanViewAnnouncementGroup]
    serializer_class = AnnouncementGroupSerializer

    def get_queryset(self):
        admin_id = self.request.user.id
        qs = AnnouncementGroup.objects.filter(admin_id=admin_id)
        return qs
    

class JoinAnnouncementGroupView(generics.GenericAPIView):
    permission_classes = [CanViewAnnouncementGroup]
    serializer_class = JoinAnnouncementGroupsSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data.get('group')
        if group is None:
            raise exceptions.ValidationError({'group': 'This field is required.'})
        
        user = self.request.user
        if user in group.members.all():
            raise exceptions.APIException('User already in group')
        
        group.members.add(user)
        group.total_members += 1
        group.save()

        return Response({'msg':'Successfully joined the announcement group'},status=status.HTTP_200_OK)