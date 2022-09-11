from django.core.exceptions import ValidationError


def checkABN(value):
    if not value.isnumeric():
        raise ValidationError("非法输入，包含非数字。")
    elif len(value) != 11:
        raise ValidationError("非法输入，只支持11位数字。")
    digits = [int(c) for c in value]
    digits[0] -= 1
    weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    checksum = sum(d * w for d, w in zip(digits, weights)) % 89
    valid = (checksum == 0)
    if valid:
        return value
    raise ValidationError("您输入的ABN无效，请检查输入是否正确。")