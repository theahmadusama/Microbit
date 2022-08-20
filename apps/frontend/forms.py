# import form class from django
from django import forms

# import GeeksModel from models.py
from ..home.models import GetAQuote


# create a ModelForm
class GetAQuoteForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = GetAQuote
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super(GetAQuoteForm, self).__init__(*args, **kwargs)
    #     self.fields['order_status'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['user'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['request_for_quote'].widget.attrs.update({'class': 'form-control'})

    def __init__(self, *args, **kwargs):
        super(GetAQuoteForm, self).__init__(*args, **kwargs)
        self.fields['order_status'].widget.attrs.update({'class': 'form-control'})

        # you can iterate all fields here
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control'
