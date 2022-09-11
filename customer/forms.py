from django import forms
from .models import Customer


class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(CreateCustomerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
