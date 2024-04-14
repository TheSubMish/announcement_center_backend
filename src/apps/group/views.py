from rest_framework import generics,exceptions,status,permissions
from rest_framework.response import Response
from .serializers import (
    CreateAnnouncementGroupSerializer,
    UpdateAnnouncementGroupSerializer,
    AnnouncementGroupSerializer,
    JoinAnnouncementGroupsSerializer,
    RatingSerializer,
)
from .permissions import (
    CanCreateAnnouncementGroup,
    CanUpdateAnnouncementGroup,
    CanDeleteAnnouncementGroup,
    CanViewAnnouncementGroup,
)
from .filters import AnnouncementGroupFilter
from .models import AnnouncementGroup,Rating
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
    queryset = AnnouncementGroup.objects.all()
    serializer_class = AnnouncementGroupSerializer
    filterset_class = AnnouncementGroupFilter

    def get_queryset(self):
        return AnnouncementGroup.objects.all()

    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    'group_id':'string (uuid)',
                    'name':'string',
                    'description':'string', 
                    'image':'image file', 
                    'average_rating':'float',
                    'category':'string',
                    'joined':'boolean',
                    'admin_id':'string(uuid)',
                    'members':'array of user id',
                    'total_members':'number',
                    'created_at':'Date time'
                }
            }
        }
    )
    def get(self, request, *args, **kwargs):
        qs = AnnouncementGroup.objects.all()
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page,many=True)
        return self.get_paginated_response(serializer.data)
    
class RetrieveAnnouncementGroupView(generics.RetrieveAPIView):
    queryset = AnnouncementGroup.objects.all()
    serializer_class = AnnouncementGroupSerializer
    
    def get_object(self):
        group_id = self.kwargs['pk']
        try:
            announcement_group = AnnouncementGroup.objects.get(group_id=group_id)
        except AnnouncementGroup.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement group does not exist'})
        return announcement_group

class ListUserCreatedAnnouncementGroupView(generics.ListAPIView):
    permission_classes = [CanViewAnnouncementGroup]
    queryset = AnnouncementGroup.objects.all()
    serializer_class = AnnouncementGroupSerializer
    filterset_class = AnnouncementGroupFilter

    def get_queryset(self):
        admin_id = self.request.user.id
        qs = AnnouncementGroup.objects.filter(admin_id=admin_id)
        return qs
    
    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    'group_id':'string (uuid)',
                    'name':'string',
                    'description':'string', 
                    'image':'image file', 
                    'category':'string',
                    'average_rating':'float',
                    'joined':'boolean',
                    'admin_id':'string(uuid)',
                    'members':'array of user id',
                    'total_members':'number',
                    'created_at':'Date time'
                }
            }
        }
    )
    def get(self, request, *args, **kwargs):
        admin_id = self.request.user.id
        qs = AnnouncementGroup.objects.filter(admin_id=admin_id)
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page,many=True)
        return self.get_paginated_response(serializer.data)


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
        if user is None:
            raise exceptions.APIException('User is not logged in')
        
        if user in group.members.all():
            raise exceptions.APIException('User already in group')
        
        group.members.add(user)
        group.total_members += 1
        group.save()

        return Response({'msg':'Successfully joined the announcement group'},status=status.HTTP_200_OK)


class ListUserJoinedAnnouncementGroupView(generics.GenericAPIView):
    permission_classes = [CanViewAnnouncementGroup]
    queryset = AnnouncementGroup.objects.all()
    serializer_class = AnnouncementGroupSerializer
    filterset_class = AnnouncementGroupFilter

    def get_queryset(self):
        user = self.request.user
        qs = AnnouncementGroup.objects.filter(members__pk=user.pk)
        return qs

    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    'group_id':'string (uuid)',
                    'name':'string',
                    'description':'string', 
                    'image':'image file', 
                    'category':'string',
                    'average_rating':'float',
                    'joined':'boolean',
                    'admin_id':'string(uuid)',
                    'members':'array of user id',
                    'total_members':'number',
                    'created_at':'Date time'
                }
            }
        }
    )
    def get(self, request, *args, **kwargs):
        user = self.request.user
        qs = AnnouncementGroup.objects.filter(members=user)
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page,many=True)
        return self.get_paginated_response(serializer.data)
    

class LeaveAnnouncementGroupView(generics.GenericAPIView):
    permission_classes = [CanViewAnnouncementGroup]
    serializer_class = JoinAnnouncementGroupsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data.get('group')
        if group is None:
            raise exceptions.ValidationError({'group': 'This field is required.'})
        
        user = self.request.user
        if user is None:
            raise exceptions.APIException('User is not logged in')
        
        if user not in group.members.all():
            raise exceptions.APIException('User not found group in group')

        group.members.remove(user)
        group.total_members -= 1
        group.save()

        return Response({'msg':'Successfully left the announcement group'},status=status.HTTP_200_OK)
    

class GiveRatingView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RatingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data.get('group')
        user = serializer.validated_data.get('user')

        try:
            rating = Rating.objects.get(user=user,group=group)
            rating.rating = serializer.validated_data.get('rating')
            rating.save()
        except Rating.DoesNotExist:
            serializer.save()

        return Response({'msg':'Group Rated succesfully'},status=status.HTTP_201_CREATED)
    
class RetrieveRatingView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

    def get_object(self):
        group_id = self.kwargs['pk']
        user = self.request.user

        try:
            group = AnnouncementGroup.objects.get(group_id=group_id)
        except AnnouncementGroup.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement group does not exist'})
        
        try:
            rating = Rating.objects.get(group=group,user=user)
        except Rating.DoesNotExist:
            raise exceptions.APIException({'error': 'Rating does not exist'})
        return rating