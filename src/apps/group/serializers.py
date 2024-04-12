from rest_framework import serializers,exceptions
from src.apps.group.models import AnnouncementGroup

class CreateAnnouncementGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementGroup
        fields = (
            'name',
            'description', 
            'image', 
            'category'
        )

    def create(self, validated_data):
        name = validated_data.get('name',None)
        description = validated_data.get('description',None)
        image = validated_data.get('image',None)
        category = validated_data.get('category',None)
        admin = self.context['request'].user

        announcement_group = AnnouncementGroup.objects.create(
            name=name,
            description=description,
            image=image,
            category=category,
            admin_id=admin.id,
        )

        announcement_group.members.add(admin)
        announcement_group.save()
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
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.image = validated_data.get('image',instance.image)
        instance.category = validated_data.get('category',instance.category)
        instance.save()
        return instance
    

class AnnouncementGroupSerializer(serializers.ModelSerializer):
    joined = serializers.SerializerMethodField()

    class Meta:
        model = AnnouncementGroup
        fields = (
            'group_id',
            'name',
            'description', 
            'image', 
            'category',
            'joined',
            'admin_id',
            'members',
            'total_members',
            'rating',
            'created_at'
        )

    def get_joined(self,obj):
        member = self.context['request'].user
        if member and member.is_authenticated:
            return member in obj.members.all()

        return False

class JoinAnnouncementGroupsSerializer(serializers.Serializer):
    group_id = serializers.UUIDField(required=True)

    def validate(self, attrs):
        group_id = attrs.get('group_id',None)
        if group_id is None:
            raise exceptions.ValidationError({'group_id': 'This field is required.'})
        
        try:
            group = AnnouncementGroup.objects.get(group_id=group_id)
            attrs['group'] = group

        except AnnouncementGroup.DoesNotExist:
            attrs['group'] = None
            raise exceptions.APIException("Group does not exist")

        return attrs