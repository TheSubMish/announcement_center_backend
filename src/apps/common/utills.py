import os,re
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.conf import settings
from celery import shared_task
from .models import SpamWord

def image_validate(image):
    check_exts = (".jpg", ".jpeg", ".png")
    file_extension= os.path.splitext(str(image))
    if image.size >= 1000000:
        raise ValidationError("File should less than 1MB")
    if file_extension[1] == check_exts[0] or file_extension[1] == check_exts[1] or file_extension[1] == check_exts[2]:
        pass
    else:
        raise ValidationError("Provide Valid Image file such as jpeg, jpg, png")
    if image:
        pass
    else:
        raise ValidationError("Image is not provided")
    
def get_user_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = request.META.get("REMOTE_ADDR")
    return x_forwarded_for if x_forwarded_for else ip

@shared_task
def send_user_mail(subject,recipients,message):
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=recipients
    )
    mail.send()


class SpamWordDetect:
    def __init__(self,text):
        self.text = text
        self.spam_words = SpamWord.objects.all()

    def is_spam(self):
        for spam_word in self.spam_words:
            if spam_word.word in self.text:
                return True
        return False
    
    def change_spam_word(self):
        for word in self.spam_words:
            pattern = rf"\b{word}\b"  # Word boundary for accurate matching
            new_paragraph = re.sub(pattern, '****', self.text, flags=re.IGNORECASE)  # Case-insensitive
            self.text = new_paragraph
        return self.text