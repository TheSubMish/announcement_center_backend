from rest_framework import serializers,exceptions
from src.apps.group.models import AnnouncementGroup,Rating,GroupMember,Role
from src.apps.common.utills import SpamWordDetect
import logging
from django.db import transaction

logger = logging.getLogger('info_logger')

class CreateAnnouncementGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementGroup
        fields = (
            'id',
            'name',
            'description', 
            'image', 
            'category',
        )

    def create(self, validated_data):
        name = validated_data.get('name',None)
        description = validated_data.get('description',None)
        image = validated_data.get('image',None)
        category = validated_data.get('category',None)

        detector = SpamWordDetect(description)
        if detector.is_spam():
            description = detector.change_spam_word()

        admin = self.context.get('request').user

        with transaction.atomic():
            announcement_group = AnnouncementGroup.objects.create(
                name=name,
                description=description,
                image=image,
                category=category,
                admin=admin,
            )
            group_member = GroupMember.objects.create(group=announcement_group,user=admin,role=Role.ADMIN)
        return announcement_group
    
class UpdateAnnouncementGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementGroup
        fields = (
            'name',
            'description', 
            'image', 
            'category'
        )

    def update(self, instance, validated_data):
        if validated_data.get('name') != instance.name:
            # If 'name' field is being updated, ensure uniqueness
            if AnnouncementGroup.objects.exclude(id=instance.id).filter(name=validated_data['name']).exists():
                logger.warning(f'Announcement group with name "{instance.name}" already exists')
                raise serializers.ValidationError({'name': 'An AnnouncementGroup with this name already exists.'})
            instance.name = validated_data['name']

        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        logger.info('Group updated successfully {instance.name}')
        return instance
    

class AnnouncementGroupSerializer(serializers.ModelSerializer):
    joined = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = AnnouncementGroup
        fields = (
            'group_id',
            'name',
            'description', 
            'image', 
            'category',
            'average_rating',
            'joined',
            'admin',
            'total_members',
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
    
class JoinAnnouncementGroupSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GroupMember
        fields = ['group','user','role']
    
    def validate(self, attrs):
        group = attrs.get('group',None)
        user = attrs.get('user',None)
        role = attrs.get('role',None)

        if group is None:
            logger.warning('Group does not exist')
            raise exceptions.ValidationError({'group': 'This field is required.'})
        
        if user is None:
            logger.warning('User does not exist')
            raise exceptions.ValidationError({'user': 'This field is required.'})
        
        if role is None:
            logger.warning('Role does not exist')
            raise exceptions.ValidationError({'role': 'This field is required.'})
        
        if GroupMember.objects.filter(group=group,user=user).exists():
            logger.warning('User is already a member of this group')
            raise exceptions.ValidationError({'user': 'User is already a member of this group'})
        
        attrs['group'] = group
        attrs['user'] = user
        attrs['role'] = role
        
        return attrs
    
    def create(self, validated_data):
        group = validated_data.get('group',None)
        user = validated_data.get('user',None)
        role = validated_data.get('role',None)

        group_member_ship = GroupMember.objects.create(
            group=group,
            user=user,
            role=role,
        )

        group.total_members += 1
        group.save()
        return group_member_ship
    
class LeaveAnnouncementGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMember
        fields = ['group','user','role']

    def validate(self, attrs):
        group = attrs.get('group',None)
        user = attrs.get('user',None)
        role = attrs.get('role',None)

        if group is None:
            logger.warning('Group does not exist')
            raise exceptions.ValidationError({'group': 'This field is required.'})
        
        if user is None:
            logger.warning('User does not exist')
            raise exceptions.ValidationError({'user': 'This field is required.'})
        
        if role is None:
            logger.warning('Role does not exist')
            raise exceptions.ValidationError({'role': 'This field is required.'})
        
        if role is Role.ADMIN:
            logger.warning('Admin cannot leave group')
            raise exceptions.ValidationError({'user': 'Admin cannot leave group'})
        
        attrs['group'] = group
        attrs['user'] = user
        attrs['role'] = role
        
        return attrs
    

class RatingSerializer(serializers.ModelSerializer):

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
    admin = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GroupMember
        fields = '__all__'

    def validate(self, attrs):
        group = attrs.get('group',None)
        user = attrs.get('user',None)
        role = attrs.get('role',None)

        if group is None:
            logger.warning('Group does not exist')
            raise exceptions.ValidationError({'group': 'This field is required.'})
        
        if user is None:
            logger.warning('User does not exist')
            raise exceptions.ValidationError({'user': 'This field is required.'})
        
        if role is None:
            logger.warning('Role does not exist')
            raise exceptions.ValidationError({'role': 'This field is required.'})
        
        if self.admin != group.admin:
            logger.warning(f'{self.admin.username} is not admin of group {group.name}')
            raise exceptions.ValidationError({'user': 'User is not admin of group'})
        
        attrs['group'] = group
        attrs['user'] = user
        attrs['role'] = role
        
        return attrs