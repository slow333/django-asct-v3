from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='사용자명')
    email = forms.EmailField(label='이메일')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = '이름은 3자 이상을 넣으세요'
        self.fields['password1'].help_text = '<ul>' \
            '<li>암호는 8자 이상입니다.</li>'\
            '<li>암호는 username하고 유사하면 안되요.</li>'\
            '<li>암호는 숫자만으로 구성되면 안되요.</li>'\
            '<li>암호는 일반적으로 사용되는 것은 안되요.</li>'\
        '</ul>'
        self.fields['password2'].help_text = '위에 암호와 같은 암호를 적으세요.'
        error_messages = {
            'username': {
                'required': '사용자명은 필수입니다.!',
            },
            'email': {
                'required': '이메일은 필수입니다.!',
            },
        }
    error_messages = {
        'password_mismatch': "암호는 2개가 같아야 합니다.",
    }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

