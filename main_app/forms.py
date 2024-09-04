from django import forms
from main_app.models import *
from captcha.fields import CaptchaField, CaptchaTextInput
from django.contrib.auth.forms import PasswordChangeForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=12,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class': 'form-control'}))


class UserForm(forms.ModelForm):
    GENDER = ((0, '男'), (1, '女'))
    username = forms.CharField(label="用户名", max_length=12, widget=forms.TextInput(attrs={'class': "form-control"}))
    gender = forms.ChoiceField(label="性别", choices=GENDER, widget=forms.Select(attrs={'class': 'form-control'}))
    user_type = forms.CharField(label="用户类型", widget=forms.TextInput(
        attrs={"class": "form-control", "readonly": "readonly"}))
    email = forms.EmailField(label="邮箱", widget=forms.EmailInput(
        attrs={"class": "form-control", "readonly": "readonly"}))
    self = forms.CharField(label="自我简介",
                           widget=forms.Textarea(attrs={"class": 'form-control', 'placeholder': '最多150字!'}))

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            instance = kwargs.get('instance').user.__dict__
            for field in self.Meta.fields:
                self.fields[field].initial = instance.get(field)

    def clean_username(self):
        form_username = self.cleaned_data.get('username')
        if self.instance is None:
            if CustomUser.objects.filter(username=form_username).exists():
                raise forms.ValidationError(
                    "该用户名已被注册!"
                )
        else:
            db_username = self.instance.user.username
            if db_username != form_username:
                if CustomUser.objects.filter(username=form_username).exists():
                    raise forms.ValidationError(
                        "该用户名已被注册!"
                    )
        return form_username

    class Meta:
        model = CustomUser
        fields = ['username', 'gender', 'user_type', 'email', 'self']


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="旧密码", widget=forms.PasswordInput(attrs={'class': "form-control"}))
    new_password1 = forms.CharField(label="新密码", widget=forms.PasswordInput(attrs={'class': "form-control"}))
    new_password2 = forms.CharField(label="确认新密码", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)


class ChangeEmailForm(forms.Form):
    email = forms.CharField(label="请输入新修改的邮箱", widget=forms.EmailInput(attrs={'class': "form-control"}))

    def clean_email(self):
        form_email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=form_email).exists():
            raise forms.ValidationError("该邮箱已存在!")
        return form_email


class RegisterForm(forms.Form):
    GENDER = ((0, '男'), (1, '女'))
    USER_TYPE = ((0, 'student'), (1, 'teacher'))
    user_type = forms.ChoiceField(choices=USER_TYPE,
                                  widget=forms.Select(attrs={'class': 'form-control', 'default': 'student'}))
    gender = forms.ChoiceField(choices=GENDER, widget=forms.Select(attrs={'class': 'form-control', 'default': 'male'}))
    username = forms.CharField(max_length=12,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': '请输入密码'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': '请确认密码'}))
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        form_username = self.cleaned_data['username'].lower()
        if CustomUser.objects.filter(username=form_username).exists():
            raise forms.ValidationError("该用户名已被注册!")
        return form_username

    def clean_email(self):
        form_email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=form_email).exists():
            raise forms.ValidationError('该邮箱已被注册!')
        return form_email

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']
        if password != confirm_password:
            raise forms.ValidationError("两次密码输入不同!")
        return confirm_password


class EditUsernameForm(forms.Form):
    # manager编辑学生的表单
    """
    呈现的信息:
    username
    email
    """
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入新的用户名'}))

    def clean_username(self):
        form_username = self.cleaned_data['username'].lower()
        if CustomUser.objects.filter(username=form_username).exists():
            raise forms.ValidationError("该用户名已被注册!")
        return form_username


class EditEmailForm(forms.Form):
    email = forms.CharField(label='邮箱',
                            widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '输入新的邮箱'}))

    def clean_email(self):
        form_email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=form_email).exists():
            raise forms.ValidationError('该邮箱已被注册!')
        return form_email
