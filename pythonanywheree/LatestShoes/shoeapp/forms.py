# # from django import forms
# # from .models import *
# #
# # class user_profile(forms.ModelForm):
# #     class Meta:
# #         model = User  # noqa
# #         fields = ['fname', 'email', 'lname',  ]
# #         widgets = {
# #             'lname': forms.TextInput(
# #                 attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product name'}),
# #             'email': forms.TextInput(
# #                 attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product email address'}),
# #             'lname': forms.TextInput(
# #                 attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product Phone number'}),
#             }

from django import forms
from .models import BookingAddress
from .models import User

class UserProfileform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fname', 'lname', 'email', 'gender']  # Adjust based on your model


class BookingAddress(forms.ModelForm):
    class Meta:
        model = BookingAddress  # noqa: F405
        fields = ['address','country','state','pincode','email','phone']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product house name'}),
            'country': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter counter'}),
            'state': forms.TextInput(attrs={'class': 'form-control form-manual input','placeholder': 'Enter state'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter Pincode'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter phone number'})
         }