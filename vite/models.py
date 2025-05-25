import cloudinary
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from cloudinary.models import CloudinaryField
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File
import os

class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    full_name = models.CharField(max_length=100, blank=True)
    profile_picture = CloudinaryField('image', blank=True, null=True, default='profile_pics/default_profile.png')
    cover_photo = CloudinaryField('image', blank=True, null=True, default='cover_photos/default_cover.jpg')
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)
    friend_requests = models.ManyToManyField('self', symmetrical=False, blank=True, 
                                           related_name='received_friend_requests')
    blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True, 
                                         related_name='blocked_by')
    points = models.IntegerField(default=0)
    qr_code = CloudinaryField('image', blank=True, null=True)  # حقل جديد لكود QR

    def __str__(self):
        return f"@{self.username}"
        
    @property
    def has_blue_badge(self):
        return self.is_verified or self.friends.count() > 10

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # إنشاء رابط البروفايل
        profile_url = f"https://yourdomain.com/profile/{self.username}"
        qr.add_data(profile_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        
        # حفظ الصورة في Cloudinary
        result = cloudinary.uploader.upload(
            buffer.getvalue(),
            folder="qr_codes",
            public_id=f"user_{self.id}_qr",
            overwrite=True
        )
        
        self.qr_code = result['secure_url']
        self.save()
        
        return self.qr_code

    def save(self, *args, **kwargs):
        # عند إنشاء مستخدم جديد، يتم توليد كود QR
        if not self.pk or not self.qr_code:
            super().save(*args, **kwargs)  # يجب حفظ المستخدم أولاً للحصول على ID
            self.generate_qr_code()
        super().save(*args, **kwargs)
        
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField(default="")  # أو أي نص تريده
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    seen_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"من {self.sender} إلى {self.receiver}: {self.content[:30]}"
    
    def mark_as_seen(self):
        if not self.is_read:
            self.is_read = True
            self.seen_at = timezone.now()
            self.save()

class Chat(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    last_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Chat {self.id}"

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)
    video = CloudinaryField('video', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.user.username}"

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"

class SavedPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} saved {self.post.id}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('message', 'رسالة جديدة'),
        ('like', 'إعجاب'),
        ('comment', 'تعليق'),
        ('friend_request', 'طلب صداقة'),
        ('friend_accept', 'قبول الصداقة'),
    )
    
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    related_id = models.PositiveIntegerField(null=True, blank=True)  # يمكن أن يكون معرف المنشور أو الرسالة

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_notification_type_display()} لـ {self.recipient.username}"