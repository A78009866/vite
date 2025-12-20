from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post, Reel
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True, label='الاسم الكامل')
    profile_picture = forms.ImageField(required=True, label='صورة البروفيل')

    class Meta:
        model = CustomUser
        # الحقول المطلوبة فقط في مرحلة التسجيل
        fields = ('username', 'full_name', 'profile_picture')

class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=range(timezone.now().year - 100, timezone.now().year - 5)),
        required=False,
        label='تاريخ الميلاد'
    )
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, required=False, label='الجنس')
    relationship_status = forms.ChoiceField(choices=CustomUser.RELATIONSHIP_STATUS_CHOICES, required=False, label='الحالة الاجتماعية')

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'profile_picture', 'cover_photo', 'bio', 'date_of_birth', 'gender', 'relationship_status')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'profile_picture': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'cover_photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['profile_picture', 'cover_photo', 'date_of_birth', 'gender', 'relationship_status']:
            self.fields[field].required = False
