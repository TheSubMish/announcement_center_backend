from rest_framework import generics,exceptions,status,permissions
from rest_framework.response import Response
from .serializers import (
    CreateAnnouncementGroupSerializer,
    UpdateAnnouncementGroupSerializer,
    AnnouncementGroupSerializer,
    JoinAnnouncementGroupSerializer,
    LeaveAnnouncementGroupSerializer,
    RatingSerializer,
    ChangeMemberRoleSerializer,
    ListGroupMemberSerializer,
    GroupCategorySerializer,
)
from .permissions import (
    CanCreateAnnouncementGroup,
    CanUpdateAnnouncementGroup,
    CanDeleteAnnouncementGroup,
    CanViewAnnouncementGroup,
    CanChangeMemberRole,
)
from .filters import AnnouncementGroupFilter
from .models import AnnouncementGroup,Rating,GroupMember,GroupType,Category
from src.apps.common.models import Status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from drf_spectacular.types import OpenApiTypes
import logging
import os

logger = logging.getLogger('info_logger')

class CreateGroupCategoryView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GroupCategorySerializer

class ListGroupCategoryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GroupCategorySerializer
    queryset = Category.objects.all()

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
                    "category": "string",
                    "group_type": "string",
                    "location": "string",
                }
            }
        },
        parameters=[
            OpenApiParameter(
                name='group_type',
                type=OpenApiTypes.STR,
                enum=[choice[0] for choice in GroupType.choices],
                description='The type of the group: public or private.',
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Group created successfully {serializer.validated_data['name']}")
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
            logger.warning("Announcement group not found")
            raise exceptions.APIException({'error': 'Announcement group does not exist'})
        logger.info(f"Announcement group deleted {announcement_group.name}")
        return announcement_group
    
class ListAnnouncementGroupView(generics.ListAPIView):
    serializer_class = AnnouncementGroupSerializer
    filterset_class = AnnouncementGroupFilter

    def get_queryset(self):
        queryset = AnnouncementGroup.objects.filter(status=Status.ACTIVE)
        filtered_queryset = self.filter_queryset(queryset)
        return filtered_queryset

    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    'group_id':'string (uuid)',
                    'name':'string',
                    'description':'string', 
                    'image':'image file', 
                    'admin':'string',
                    'category':'string',
                    'group_type': 'string',
                    'total_members':'number',
                    'location': 'string',
                    'invite_code':'string',
                    'code_expires_at':'Date time',
                    'average_rating':'float',
                    'joined':'boolean',
                    'created_at':'Date time'
                }
            }
        },
        parameters=[
            OpenApiParameter(
                name='group_type',
                type=OpenApiTypes.STR,
                enum=[choice[0] for choice in GroupType.choices],
                description='The type of the group: public or private.',
            ),
            OpenApiParameter(
                name="q",
                location=OpenApiParameter.QUERY,
                description="search query for group",
                required=False,
                type=str,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        # get searched announcement groups
        searchTerm = self.request.query_params.get("q", "")  # type:ignore
        if searchTerm :
            if str(os.environ.get("USE_POSTGRES")).lower() == "false":
                queryset = AnnouncementGroup.objects.filter(title__icontains=searchTerm)
            else:
                search_vector = SearchVector("name",)
                search_query = SearchQuery(searchTerm)
                queryset = AnnouncementGroup.objects.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                ).filter(search=search_query)
            
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)

        if self.pagination_class:
            page = self.paginate_queryset(filtered_queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
    
class RetrieveAnnouncementGroupView(generics.RetrieveAPIView):
    queryset = AnnouncementGroup.objects.all()
    serializer_class = AnnouncementGroupSerializer
    
    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    'group_id':'string (uuid)',
                    'name':'string',
                    'description':'string', 
                    'image':'image file', 
                    'admin':'string',
                    'category':'string',
                    'group_type': 'string',
                    'total_members':'number',
                    'location': 'string',
                    'invite_code':'string',
                    'code_expires_at':'Date time',
                    'average_rating':'float',
                    'joined':'boolean',
                    'created_at':'Date time'
                }
            }
        },
        parameters=[
            OpenApiParameter(
                name='group_type',
                type=OpenApiTypes.STR,
                enum=[choice[0] for choice in GroupType.choices],
                description='The type of the group: public or private.',
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        group_id = self.kwargs['pk']
        try:
            announcement_group = AnnouncementGroup.objects.get(group_id=group_id,status=Status.ACTIVE)
        except AnnouncementGroup.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement group does not exist'})
        
        serializer = self.get_serializer(instance=announcement_group)
        return Response(serializer.data)


class ListUserCreatedAnnouncementGroupView(generics.ListAPIView):
    permission_classes = [CanViewAnnouncementGroup]
    queryset = AnnouncementGroup.objects.all()
    serializer_class = AnnouncementGroupSerializer
    filterset_class = AnnouncementGroupFilter

    def get_queryset(self):
        admin_id = self.request.user.id
        qs = AnnouncementGroup.objects.filter(admin_id=admin_id,status=Status.ACTIVE)
        return qs
    
    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    'group_id':'string (uuid)',
                    'name':'string',
                    'description':'string', 
                    'image':'image file', 
                    'admin':'string',
                    'category':'string',
                    'group_type': 'string',
                    'total_members':'number',
                    'location': 'string',
                    'invite_code':'string',
                    'code_expires_at':'Date time',
                    'average_rating':'float',
                    'joined':'boolean',
                    'created_at':'Date time'
                }
            }
        },
        parameters=[
            OpenApiParameter(
                name='group_type',
                type=OpenApiTypes.STR,
                enum=[choice[0] for choice in GroupType.choices],
                description='The type of the group: public or private.',
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)

        if self.pagination_class:
            page = self.paginate_queryset(filtered_queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)


class JoinAnnouncementGroupView(generics.CreateAPIView):
    permission_classes = [CanViewAnnouncementGroup]
    serializer_class = JoinAnnouncementGroupSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        group = serializer.validated_data['group']
        user = serializer.validated_data['user']
        logger.info(f"{user.username} joined group {group.name}")
        return Response({'msg':'Successfully joined the announcement group'},status=status.HTTP_200_OK)


class ListUserJoinedAnnouncementGroupView(generics.GenericAPIView):
    permission_classes = [CanViewAnnouncementGroup]
    queryset = AnnouncementGroup.objects.all()
    serializer_class = AnnouncementGroupSerializer
    filterset_class = AnnouncementGroupFilter

    def get_queryset(self):
        user = self.request.user
        group_ids = GroupMember.objects.filter(user=user, status=Status.ACTIVE).values_list('group_id', flat=True)
        qs = AnnouncementGroup.objects.filter(group_id__in=group_ids,status=Status.ACTIVE)        
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
        ,
        parameters=[
            OpenApiParameter(
                name='group_type',
                type=OpenApiTypes.STR,
                enum=[choice[0] for choice in GroupType.choices],
                description='The type of the group: public or private.',
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)

        if self.pagination_class:
            page = self.paginate_queryset(filtered_queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
    

class LeaveAnnouncementGroupView(generics.GenericAPIView):
    permission_classes = [CanViewAnnouncementGroup]
    serializer_class = LeaveAnnouncementGroupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data['group']
        user = serializer.validated_data['user']
        logger.info(f'{user.username} left group {group.name}')
        return Response({'msg':'Successfully left the announcement group'},status=status.HTTP_200_OK)
    
class ChangeMemberRoleView(generics.UpdateAPIView):
    permission_classes = [CanChangeMemberRole]
    serializer_class = ChangeMemberRoleSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_member = serializer.validated_data.get('group_member')
        
        group_member.role = serializer.validated_data.get('role')
        group_member.save()

        return Response({'msg':'Member role updated successfully'},status=status.HTTP_200_OK)
    
class ListGroupMemberView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = GroupMember.objects.all()
    serializer_class = ListGroupMemberSerializer

    def get(self, request,*args, **kwargs):
        group_id = self.kwargs['pk']
        try:
            announcement_group = AnnouncementGroup.objects.get(group_id=group_id)
        except AnnouncementGroup.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement group does not exist'})
        
        group_members = GroupMember.objects.filter(group=announcement_group,status=Status.ACTIVE)
        
        if self.pagination_class:
            page = self.paginate_queryset(group_members)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(group_members, many=True)
        return Response(serializer.data)
    
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
            logger.info(f'{user.username} updated their rating ({serializer.validated_data["rating"]}) to group {group.name}')
        except Rating.DoesNotExist:
            logger.info(f'{user.username} rated ({serializer.validated_data["rating"]}) to group {group.name}')
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