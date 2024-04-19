from rest_framework import serializers,exceptions
from src.apps.group.models import AnnouncementGroup,Rating
from src.apps.common.utills import SpamWordDetect

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

        detector = SpamWordDetect(description)
        if detector.is_spam():
            description = detector.change_spam_word()

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
            'admin_id',
            'members',
            'total_members',
            'created_at'
        )

    def get_joined(self,obj):
        member = self.context['request'].user
        if member and member.is_authenticated:
            return member in obj.members.all()

        return False
    
    def get_average_rating(self, obj):
        average_rating = obj.average_rating()  # Call the method from the model
        return average_rating if average_rating else 0.0

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
    
class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'

    def validate(self, attrs):
        group = attrs.get('group',None)
        user = attrs.get('user',None)
        rating = attrs.get('rating',None)

        if group is None:
            raise exceptions.ValidationError({'group': 'This field is required.'})
        
        if user is None:
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