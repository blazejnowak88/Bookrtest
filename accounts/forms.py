from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', ]

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('re_password')
        if p1 is None or p2 is None or p1 != p2:
            raise ValidationError('Hasła musza być te same')
        return cleaned_data


class GroupPermissionAddForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')
        widgets = {
            'permissions': forms.CheckboxSelectMultiple
        }


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False,
                                  choices=(
                                      ("title", "Title"),
                                      ("contributor", "Contributor")
                                  ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.form_method = "get"
        # self.helper.add_input(Submit("", "Search"))

    def clean_search_in(self):
        return self.cleaned_data["search_in"] or "title"
