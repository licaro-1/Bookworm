from django import forms


def validate_image(image):
    """
    Form image validator
    max-size = 1 MB
    format: jpeg, png, jpg.
    """
    content_type = image.content_type
    max_size = 1024 * 1024
    if content_type not in ["image/jpeg", "image/png"]:
        raise forms.ValidationError(
            "Некорректный формат обложки"
        )
    if image.size > max_size:
        raise forms.ValidationError(
            "Максимальный размер обложки - 1 МБ"
        )
    return image
