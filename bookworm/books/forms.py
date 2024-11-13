from django import forms
from tinymce.widgets import TinyMCE

from bookworm.settings import S3_DIR_BOOK_COVERS
from utils.form_validation import validate_image
from s3.client import bookworm_s3_client
from books.models import Book, Comment
from books.service import book_service


class BookCreateForm(forms.ModelForm):
    image = forms.FileField()
    description = forms.CharField(
        widget=forms.Textarea,
    )

    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "publication_year",
            "description",
        )

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data["title"]
        book_with_title_exists = book_service.book_ty_title_exists(title)
        if book_with_title_exists:
            raise forms.ValidationError(
                f"Книга с названием {title!r} уже существует."
            )
        return title

    def clean_image(self):
        image = self.cleaned_data["image"]
        return validate_image(image)

    def save(self, commit=True):
        book = super().save(commit=False)
        book.creator = self.creator
        image_file = self.cleaned_data["image"]
        buffer_file = bookworm_s3_client.read_file(image_file)
        uploaded_filename = bookworm_s3_client.upload_file(
            buffer_file,
            image_file.name,
            S3_DIR_BOOK_COVERS
        )
        book.image = uploaded_filename
        if commit:
            book.save()
        return book


class CommentCreateForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 10}))

    class Meta:
        model = Comment
        fields = ("text", "rating", "recommended")
