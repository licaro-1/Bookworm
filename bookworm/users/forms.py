from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField

from bookworm.settings import (
    S3_DIR_USER_IMAGES,
    DEFAULT_USER_AVATAR_IMG
)
from utils.form_validation import validate_image
from s3.client import bookworm_s3_client
from logger.log import logger
from users.service import user_service


User = get_user_model()


class CreationForm(forms.ModelForm):
    captcha = ReCaptchaField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email:
            raise forms.ValidationError(
                "Почта обязательна для регистрации"
            )
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Почта уже занята"
            )
        if not username:
            raise forms.ValidationError(
                "Юзернейм обязателен для регистрации"
            )
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Юзернейм уже занят")
        # Check if password is strong enough
        if len(password) < 8:
            raise forms.ValidationError(
                "Длина пароля должна быть не менее 8 символов"
            )
        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    pass


class UserUpdateForm(forms.ModelForm):
    avatar = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            return validate_image(avatar)
        return None

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if (
                username != self.instance.username.strip()
                and
                user_service.check_user_exists_by_username(username)
        ):
            raise forms.ValidationError(f"Юзернейм {username} уже занят")
        return username

    def save(self, commit=True):
        logger.info(f"Start updating profile {self.instance.email}")
        if self.cleaned_data.get("avatar"):
            avatar = self.cleaned_data["avatar"]
            validate_image(avatar)
            if self.instance.avatar != DEFAULT_USER_AVATAR_IMG:
                try:
                    bookworm_s3_client.delete_file_from_s3(
                        self.instance.avatar,
                        S3_DIR_USER_IMAGES
                    )
                except Exception as er:
                    logger.warning(
                        f"Ошибка удаления прошлого аватара пользователя {er}"
                    )
            buffer = bookworm_s3_client.read_file(
                avatar
            )
            file_name = bookworm_s3_client.upload_file(
                buffer,
                avatar.name,
                S3_DIR_USER_IMAGES
            )
            self.instance.avatar = file_name
            logger.info(
                f"Update user-{self.instance.email} avatar"
                f" to {self.instance.avatar}"
            )
        for field in ["username", "first_name", "last_name"]:
            if getattr(self.instance, field) != self.cleaned_data[field]:
                setattr(self.instance, field, self.cleaned_data[field])
        if commit:
            self.instance.save()
        return self.instance
