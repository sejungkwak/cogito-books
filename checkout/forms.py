from django import forms

from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import Order


# Resouce: Vladimort's answer on StackOverflow
# https://stackoverflow.com/questions/67429771
class CustomPhoneNumberPrefixWidget(PhoneNumberPrefixWidget):
    """
    Allow to access each element of the phone number fields in html.
    """

    def subwidgets(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        return context['widget']['subwidgets']


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
        widgets = {
            'phone_number': CustomPhoneNumberPrefixWidget()
        }

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

        self.fields['email'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].label = False

            if field == 'phone_number':
                order_widgets = self.fields['phone_number'].widget.widgets
                order_widgets[0].attrs.update({'class': 'col-4 form-select'})
                order_widgets[1].attrs.update({'class': 'col-8 form-control'})

            if field != 'country':
                if not self.fields[field].required:
                    placeholder = f'{placeholders[field]} (Optional)'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

            if field not in ['phone_number', 'country']:
                self.fields[field].widget.attrs.update({'class': 'form-select'
                                                        })
