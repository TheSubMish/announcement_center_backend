from rest_framework import serializers,exceptions
from src.apps.group.models import AnnouncementGroup,Rating,GroupMember,Role,GroupType,Category
from src.apps.auth.serializers import UserSerializer
from src.apps.common.serializers import DynamicSerializer
from src.apps.common.utills import SpamWordDetect
from src.apps.common.models import Status
import logging
from django.db import transaction
from django.utils.crypto import get_random_string
from django.utils import timezone

logger = logging.getLogger('info_logger')

class GroupCategorySerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ('id','name', 'created_by')

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Category with this name already exists.')
        return value

class CreateAnnouncementGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementGroup
        fields = (
            'name',
            'description', 
            'image', 
            'category',
            'group_type',
            'location',
        )

    def create(self, validated_data):
        name = validated_data.get('name',None)
        description = validated_data.get('description',None)
        image = validated_data.get('image',None)
        admin = self.context.get('request').user
        category = validated_data.get('category',None)
        group_type = validated_data.get('group_type',None)
        location = validated_data.get('location',None)

        if AnnouncementGroup.objects.filter(name=name).exists():
            logger.warning(f'Announcement group with name "{name}" already exists')
            raise serializers.ValidationError({'name': 'Group with this name already exists.'})
        
        invite_code = None
        code_expires_at = None
        if group_type == GroupType.PRIVATE:
            invite_code = get_random_string(length=5)
            code_expires_at = timezone.now() + timezone.timedelta(days=7)

        detector = SpamWordDetect(description)
        if detector.is_spam():
            description = detector.change_spam_word()

        with transaction.atomic():
            announcement_group = AnnouncementGroup.objects.create(
                name=name,
                description=description,
                image=image,
                category=category,
                admin=admin,
                group_type=group_type,
                total_members=1,
                location=location,
                invite_code=invite_code,
                code_expires_at=code_expires_at    
            )
            GroupMember.objects.create(group=announcement_group,user=admin,role=Role.ADMIN)
        return announcement_group
    
class UpdateAnnouncementGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementGroup
        fields = (
            'name',
            'description', 
            'image', 
            'category',
            'group_type',
            'location',
        )

    def update(self, instance, validated_data):
        try:
            if validated_data.get('name') != instance.name:
                # If 'name' field is being updated, ensure uniqueness
                if AnnouncementGroup.objects.exclude(id=instance.id).filter(name=validated_data['name']).exists():
                    logger.warning(f'Announcement group with name "{instance.name}" already exists')
                    raise serializers.ValidationError({'name': 'An AnnouncementGroup with this name already exists.'})
                instance.name = validated_data['name']
        except KeyError:
            pass

        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.category = validated_data.get('category', instance.category)

        instance.group_type = validated_data.get('group_type', instance.group_type)
        if validated_data.get('group_type') == GroupType.PRIVATE:
            instance.invite_code = get_random_string(length=5)
            instance.code_expires_at = timezone.now() + timezone.timedelta(days=7)
        
        if validated_data.get('group_type') == GroupType.PUBLIC:
            instance.invite_code = None
            instance.code_expires_at = None

        instance.location = validated_data.get('location', instance.location)
        instance.save()
        logger.info('Group updated successfully {instance.name}')
        return instance
    

class AnnouncementGroupSerializer(DynamicSerializer):
    joined = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    admin = serializers.StringRelatedField()
    admin_id = serializers.SerializerMethodField()

    class Meta:
        model = AnnouncementGroup
        fields = (
            'group_id',
            'name',
            'description', 
            'image', 
            'admin',
            'admin_id',
            'category',
            'group_type',
            'total_members',
            'location',
            'invite_code',
            'code_expires_at',
            'average_rating',
            'joined',
            'created_at',
            'updated_at',
        )

    def get_joined(self,obj):
        if self.context.get('request').user.is_authenticated:
            self.user = self.context.get('request').user
            if GroupMember.objects.filter(group=obj,user=self.user).exists():
                return True
        return False
    
    def get_average_rating(self, obj):
        average_rating = obj.average_rating()  # Call the method from the model
        return average_rating if average_rating else 0.0
    
    def get_admin_id(self, obj):
        return obj.admin.id if obj.admin else None
    
    def get_rated_group(self, obj):
        if self.context.get('request').user.is_authenticated:
            self.user = self.context.get('request').user
            if Rating.objects.filter(group=obj,user=self.user).exists():
                return True
        return False
    

    def rating(self, obj):
        if self.context.get('request').user.is_authenticated:
            self.user = self.context.get('request').user
            if Rating.objects.filter(group=obj,user=self.user).exists():
                return Rating.objects.get(group=obj,user=self.user).rating
            else:
                return None
        else:
            return None
    
class JoinAnnouncementGroupSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    invite_code = serializers.CharField(max_length=10,allow_blank=True,required=False)

    class Meta:
        model = GroupMember
        fields = ['group','user','invite_code']
    
    def validate(self, attrs):
        group = attrs.get('group',None)
        user = attrs.get('user',None)
        invite_code = attrs.get('invite_code',None)

        if group is None:
            logger.warning('Group does not exist')
            raise exceptions.ValidationError({'group': 'This field is required.'})
        
        if group.group_type == GroupType.PRIVATE:
            if invite_code is None:
                logger.warning('Invite code is required')
                raise exceptions.ValidationError({'invite_code': 'This field is required.'})
            
            if group.invite_code != invite_code:
                logger.warning(f'Invalid invite code inserted by {user}')
                raise exceptions.ValidationError({'invite_code': 'Not a valid invite code.'})

            if group.code_expires_at < timezone.now():
                logger.warning('Invite code expires')
                raise exceptions.ValidationError({'invite_code': 'Invite code expires'})
        
        if user is None:
            logger.warning('User does not exist')
            raise exceptions.ValidationError({'user': 'This field is required.'})
        
        if GroupMember.objects.filter(group=group,user=user,status="active").exists():
            logger.warning('User is already a member of this group')
            raise exceptions.ValidationError({'user': 'User is already a member of this group'})
        
        attrs['group'] = group
        attrs['user'] = user
        
        return attrs
    
    def create(self, validated_data):
        group = validated_data.get('group',None)
        user = validated_data.get('user',None)

        try:
            group_member_ship = GroupMember.objects.get(group=group, user=user)
            group_member_ship.status = Status.ACTIVE
            group_member_ship.save()

        except GroupMember.DoesNotExist:

            group_member_ship = GroupMember.objects.create(
                group=group,
                user=user,
                role=Role.MEMBER,
            )

        group.total_members += 1
        group.save()
        return group_member_ship
    
class LeaveAnnouncementGroupSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    flagged = serializers.BooleanField(default=False)

    class Meta:
        model = GroupMember
        fields = ['group','user',"flagged"]

    def validate(self, attrs):
        group = attrs.get('group',None)
        user = attrs.get('user',None)
        flagged = attrs.get('flagged',False)

        if group is None:
            logger.warning('Group does not exist')
            raise exceptions.ValidationError({'group': 'This field is required.'})
        
        if user is None:
            logger.warning('User does not exist')
            raise exceptions.ValidationError({'user': 'This field is required.'})
        
        try:
            group_member = GroupMember.objects.get(user=user, group=group,status=Status.ACTIVE)
        except:
            logger.warning("User is not a member of the group")
            raise exceptions.APIException({'error': 'User is not a member of the group'})
        
        if group_member.role == Role.ADMIN:
            logger.warning("Admin cannot leave the group")
            raise exceptions.APIException({'error': 'Admin cannot leave the group'})
        
        if flagged:
            group_member.flagged = True
        
        else:
            group_member.status = Status.INACTIVE

        group.total_members = group.total_members - 1
        group.save()
        group_member.save()
        
        return attrs
    

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Rating
        fields = '__all__'

    def validate(self, attrs):
        group = attrs.get('group',None)
        user = attrs.get('user',None)
        rating = attrs.get('rating',None)

        if group is None:
            logger.warning('Group does not exist')
            raise exceptions.ValidationError({'group': 'This field is required.'})
        
        if user is None:
            logger.warning('User does not exist')
            raise exceptions.ValidationError({'user': 'This field is required.'})
        
        attrs['group'] = group
        attrs['user'] = user
        attrs['rating'] = rating
        
        return attrs

        
    def create(self, validated_data):
        group = validated_data.get('group',None)
        user = validated_data.get('user',None)
        rating = validated_data.get('rating',None)

        rating = Rating.objects.create(
            group=group,
            user=user,
            rating=rating,
        )
        return rating
    

    def update(self, instance, validated_data):
        instance.group = validated_data.get('group',instance.group)
        instance.user = validated_data.get('user',instance.user)
        instance.rating = validated_data.get('rating',instance.rating)
        instance.save()
        return instance
    
class ChangeMemberRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMember
        fields = '__all__'

    # def validate(self, attrs):
    #     group = attrs.get('group',None)
    #     user = attrs.get('user',None)
    #     role = attrs.get('role',None)

    #     if group is None:
    #         logger.warning('Group does not exist')
    #         raise exceptions.ValidationError({'group': 'This field is required.'})
        
    #     if user is None:
    #         logger.warning('User does not exist')
    #         raise exceptions.ValidationError({'user': 'This field is required.'})
        
    #     if role is None:
    #         logger.warning('Role does not exist')
    #         raise exceptions.ValidationError({'role': 'This field is required.'})
        
    #     try:
    #         group_member = GroupMember.objects.get(user=user, group=group)
    #     except:
    #         logger.warning("User is not a member of the group")
    #         raise exceptions.APIException({'error': 'User is not a member of the group'})
        
    #     group_admin = self.context['request'].user
    #     if group.admin != group_admin:
    #         logger.warning("User is not the group admin")
    #         raise exceptions.APIException({'error': 'User is not the group admin'})
        
    #     attrs['group_member'] = group_member
        
    #     return attrs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
# class ListGroupMemberSerializer(serializers.Serializer):
#     user_id = serializers.UUIDField()
#     user = serializers.CharField(max_length=255)
#     role = serializers.CharField(max_length=255)

#     def get_user_id(self,obj):
#         return obj.user.id

class ListGroupMemberSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()


    class Meta:
        model = GroupMember
        fields = '__all__'


    def get_user(self, obj):
        return UserSerializer(instance=obj.user, fields=["id","username"]).data