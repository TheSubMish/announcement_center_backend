from rest_framework import serializers
from .models import Announcement,AnnouncementComment
from src.apps.common.utills import SpamWordDetect
from src.apps.common.models import Status
import logging

logger = logging.getLogger('info_logger')

class CreateAnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = (
            'group',
            'user',
            'title',
            'description', 
            'image',
            'image_description',
            'location',
            'link',
            'contact_name',
            'contact_email',
            'announcement_visibility',
            'announcement_type',
            'date',
        )

    def create(self, validated_data):
        user = validated_data.get('user',None)
        group = validated_data.get('group',None)
        title = validated_data.get('title',None)
        description = validated_data.get('description',None)
        image = validated_data.get('image',None)
        image_description = validated_data.get('image_description',None)
        location = validated_data.get('location',None)
        link = validated_data.get('link',None)
        contact_name = validated_data.get('contact_name',None)
        contact_email = validated_data.get('contact_email',None)
        announcement_visibility = validated_data.get('announcement_visibility',None)
        announcement_type = validated_data.get('announcement_type',None)
        date = validated_data.get('date',None)

        detector = SpamWordDetect(description)
        if detector.is_spam():
            description = detector.change_spam_word()

        announcement = Announcement.objects.create(
            user=user,
            group=group,
            title=title,
            description=description,
            image=image,
            image_description=image_description,
            location=location,
            link=link,
            contact_name=contact_name,
            contact_email=contact_email,
            announcement_visibility=announcement_visibility,
            announcement_type=announcement_type,
            date=date
        )
        logger.info(f'announcement: {announcement.title} created by user: {announcement.user}')
        return announcement
    

class UpdateAnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = (
            'title',
            'description', 
            'image',
            'image_description',
            'location',
            'link',
            'contact_name',
            'contact_email',
            'announcement_visibility',
            'announcement_type',
            'date',
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.image = validated_data.get('image',instance.image)
        instance.image_description = validated_data.get('image_description',instance.image_description)
        instance.location = validated_data.get('location',instance.location)
        instance.link = validated_data.get('link',instance.link)
        instance.contact_name = validated_data.get('contact_name',instance.contact_name)
        instance.contact_email = validated_data.get('contact_email',instance.contact_email)
        instance.announcement_visibility = validated_data.get('announcement_visibility',instance.announcement_visibility)
        instance.announcement_type = validated_data.get('announcement_type',instance.announcement_type)
        instance.date = validated_data.get('date',instance.date)
        instance.save()
        logger.info(f'announcement updated: {instance.title} by user: {self.context["request"].user}')
        return instance
    
class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = '__all__'


class CreateAnnouncementCommentSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AnnouncementComment
        fields = '__all__'

    def validate(self, attrs):
        announcement = attrs.get('announcement',None)
        if announcement.status == Status.INACTIVE:
            raise serializers.ValidationError({'error': 'Announcement is inactive'})
        return super().validate(attrs)
    
    def create(self, validated_data):
        announcement = validated_data.get('announcement',None)
        user = validated_data.get('user',None)
        comment = validated_data.get('comment',None)
        parent = validated_data.get('parent',None)

        detector = SpamWordDetect(comment)
        if detector.is_spam():
            comment = detector.change_spam_word()

        announcement_comment = AnnouncementComment.objects.create(
            announcement=announcement,
            user=user,
            comment=comment,
            parent=parent,
        )
        logger.info(f'comment in announcement: {announcement.title} by user: {announcement_comment.user}')

        return announcement_comment
    
class UpdateAnnouncementCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementComment
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment',instance.comment)
        instance.save()
        logger.info(f'comment updated in announcement: {instance.announcement.title} by user: {instance.user}')
        return instance
    
class AnnouncementCommentSerializer(serializers.ModelSerializer):
    announcement = serializers.StringRelatedField()
    level = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = AnnouncementComment
        fields = '__all__'

    def get_level(self, obj):
        level = obj.get_level()
        return level
    
    def get_replies(self, obj):
        replies = obj.replies.order_by('-created_at')  # Order replies by creation time in descending order
        return AnnouncementCommentSerializer(replies, many=True).data