from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Vendor
from django import forms
from django_currentuser.middleware import get_current_user
from .models import Review


class VendorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Vendor
        fields = UserCreationForm.Meta.fields + ('business_name', 'phone_number', 'address',)
        fields = tuple(str(field) for field in fields)
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['vendor'].initial = self.instance.business_name
            self.fields['vendor'].widget.attrs['readonly'] = True
        
class VendorChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Vendor
        fields = UserCreationForm.Meta.fields + ('business_name', 'phone_number', 'address',)
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['vendor'].initial = self.instance.business_name
            self.fields['vendor'].widget.attrs['readonly'] = True
            
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'name', 'email']
