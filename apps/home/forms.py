# import form class from django
from django import forms

# import GeeksModel from models.py
from .models import GetAQuote, ExtraInfo, UserProfile


# create a ModelForm
class GetAQuoteForm(forms.ModelForm):
    class Meta:
        model = GetAQuote
        fields = "__all__"

    # upload_design = forms.FileField(widget=forms.FileInput(attrs={'accept': 'application/pdf'}))

    def __init__(self, *args, **kwargs):
        super(GetAQuoteForm, self).__init__(*args, **kwargs)
        self.fields['order_status'].widget.attrs.update({'class': 'form-control'})

        # you can iterate all fields here
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control'

# UserProfile Form

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["company_name", "company_address_1" , "company_address_2", "town", "country","postal_code", "company_vat_number", "phone_number", "company_role", "first_name", "last_name","email"]

    # upload_design = forms.FileField(widget=forms.FileInput(attrs={'accept': 'application/pdf'}))

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # self.fields['order_status'].widget.attrs.update({'class': 'form-control'})

        # you can iterate all fields here
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control'


class ExtraInfoForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = ExtraInfo
        fields = "__all__"
