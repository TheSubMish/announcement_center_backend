from rest_framework import serializers
from .models import Announcement,AnnouncementComment
from src.apps.group.models import AnnouncementGroup
from src.apps.common.utills import SpamWordDetect
from src.apps.auth.models import User

class CreateAnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = (
            'title',
            'description', 
            'image', 
            'group',
            'payment_method',
            'admin',
        )

    def create(self, validated_data):
        title = validated_data.get('title',None)
        description = validated_data.get('description',None)
        image = validated_data.get('image',None)
        payment_method = validated_data.get('payment_method',None)
        admin = self.context['request'].user
        group = validated_data.get('group',None)

        detector = SpamWordDetect(description)
        if detector.is_spam():
            description = detector.change_spam_word()

        announcement = Announcement.objects.create(
            title=title,
            description=description,
            image=image,
            payment_method=payment_method,
            admin=admin,
            group=group
        )
        return announcement
    

class UpdateAnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = (
            'title',
            'description', 
            'image', 
            'payment_method',
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.image = validated_data.get('image',instance.image)
        instance.payment_method = validated_data.get('payment_method',instance.payment_method)
        instance.save()
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

        detector = SpamWordDetect(comment)
        if detector.is_spam():
            comment = detector.change_spam_word()

        announcement_comment = AnnouncementComment.objects.create(
            announcement=announcement,
            user=user,
            comment=comment,
        )

        return announcement_comment
    
class UpdateAnnouncementCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementComment
        fields = '__all__'


    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment',instance.comment)
        instance.save()
    
        return instance
    
class AnnouncementCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementComment
        fields = '__all__'