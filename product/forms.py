from django import forms
from django.forms import Select
from sortedcontainers import SortedDict

from product.models import Product, Address, Bike


class createProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('merchant', 'address', 'status', 'view_count')

    def __init__(self, *args, **kwargs):
        super(createProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name != "image" and visible.name != "is_rent":
                visible.field.widget.attrs['class'] = 'form-control'


class createBikeForm(createProductForm):
    class Meta:
        model = Bike
        exclude = ('merchant', 'address', 'status', 'view_count')
        # fields = ['bike_size', 'bike_style', 'bike_brand', 'bike_power', 'bike_weight', 'bike_longDescription']

    def __init__(self, *args, **kwargs):
        super(createBikeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name != "image":
                visible.field.widget.attrs['class'] = 'form-control'
        self.rearrange_field_order()

    # rearrange image field as the last field of the form
    def rearrange_field_order(self):
        new_fields = {field_name: self.fields.get(field_name) for field_name in
                      self.fields if field_name != "image"}

        # then add others whose not defined in order list
        for key, value in self.fields.items():
            if key not in new_fields:
                new_fields[key] = value

        self.fields = new_fields


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
