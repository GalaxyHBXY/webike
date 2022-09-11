from django import forms
from .models import Merchant


class CreateMerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ['merchant_name']

    def __init__(self, *args, **kwargs):
        super(CreateMerchantForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
