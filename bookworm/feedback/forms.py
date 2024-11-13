from django import forms
from django_recaptcha.fields import ReCaptchaField


from feedback.models import Feedback


class FeedbackCreationForm(forms.ModelForm):
    """Form for creating Feedback."""
    file = forms.FileField(required=False)
    text = forms.CharField(
        widget=forms.Textarea,
        min_length=80
    )
    captcha = ReCaptchaField()

    class Meta:
        model = Feedback
        fields = (
            "theme",
            "text",
            "file"
        )

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("author", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        feedback = super().save(commit=False)
        feedback.author = self.author
        if commit:
            feedback.save()
            return feedback
        return feedback
