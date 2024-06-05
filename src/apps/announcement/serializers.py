from rest_framework import serializers
from .models import Announcement,AnnouncementComment
from src.apps.common.utills import SpamWordDetect
import logging

logger = logging.getLogger('info_logger')

class CreateAnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = (
            'title',
            'description', 
            'image', 
            'group',
            'user',
            'announcement_type',
            'event_date'
        )

    def create(self, validated_data):
        title = validated_data.get('title',None)
        description = validated_data.get('description',None)
        image = validated_data.get('image',None)
        announcement_type = validated_data.get('announcement_type',None)
        user = self.context['request'].user
        group = validated_data.get('group',None)
        event_date = validated_data.get('event_date',None)

        detector = SpamWordDetect(description)
        if detector.is_spam():
            description = detector.change_spam_word()

        announcement = Announcement.objects.create(
            title=title,
            description=description,
            image=image,
            announcement_type=announcement_type,
            user=user,
            group=group,
            event_date=event_date
        )
        logger.info(f'announcement created: {announcement.title} by user: {announcement.user}')
        return announcement
    

class UpdateAnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = (
            'title',
            'description', 
            'image',
            'announcement_type',
            'event_date',
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.image = validated_data.get('image',instance.image)
        instance.announcement_type = validated_data.get('announcement_type',instance.announcement_type)
        instance.event_date = validated_data.get('event_date',instance.event_date)
        instance.save()
        logger.info(f'announcement updated: {instance.title} by user: {instance.user}')
        print(logger)
        return instance
    
class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = '__all__'


class CreateAnnouncementCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementComment
        fields = '__all__'
    
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