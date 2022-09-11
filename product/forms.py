from django import forms
from django.forms import Select

from product.models import Product, Address


class createProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(createProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name != "image":
                visible.field.widget.attrs['class'] = 'form-control'


class createAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line_1', 'suburb', 'state', 'postcode']

    def __init__(self, *args, **kwargs):
        super(createAddressForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            # if visible.name == "state":
            #     visible.field.widget = Select(choices=[[Address.state, Address.state]])

# class createProductImageForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['image']
#         widgets = {
#             'image': forms.FileInput()
#         }
