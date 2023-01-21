from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    A form to get the delivery information from the shopper.
    """
    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'phone_number',
            'address_line_1',
            'address_line_2',
            'town_or_city',
            'county',
            'postcode',
            'country'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full name',
            'email': 'Email address',
            'phone_number': 'Phone number',
            'address_line_1': 'Address line 1',
            'address_line_2': 'Address line 2',
            'town_or_city': 'Town/City',
            'county': 'County/State',
            'postcode': 'postcode/ZIP',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if not self.fields[field].required:
                    placeholder = f'{placeholders[field]} (Optional)'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            else:
                self.fields[field].widget.attrs.update({'class': 'form-select'
                                                        })
            self.fields[field].label = False
