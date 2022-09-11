from django.core.exceptions import ValidationError


def file_size_limit(value):
    filesize = value.size
    print(filesize)
    if filesize > 1024 * 1024 * 2:
        raise ValidationError("The Max size of the image is 2MB")
    else:
        return value