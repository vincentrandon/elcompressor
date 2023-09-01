from django import forms
from tool.models import ImageUpload


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']


class ImageFormZip(forms.Form):
    pass


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'First name',
                                                                               'class': 'block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6'}))
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Name',
                                                                            'class': 'block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                            'class': 'block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message',
                                                           'class': 'block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6'}))
