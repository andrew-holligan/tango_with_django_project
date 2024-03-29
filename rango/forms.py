from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

# Create your models here.


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name."
    )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # inline class to provide additional info about the form
    class Meta:
        # providing association between ModelForm and a model
        model = Category
        fields = ("name",)


class PageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=Page.TITLE_MAX_LENGTH,
        help_text="Please enter the title of the page.",
    )
    url = forms.URLField(
        max_length=Page.URL_MAX_LENGTH, help_text="Please enter the URL of the page."
    )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        # hide foreign key as could include NULL values
        # we exclude the category field from the form
        exclude = ("category",)
        # we could of also specified all fields to include
        # fields = ('title', 'url', 'views')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get("url")

        # If url is not empty and doesn't start with 'http://',
        # then prepend 'http://'.
        if url and not url.startswith("http://"):
            url = f"http://{url}"
            cleaned_data["url"] = url

        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    # additional properties
    class Meta:
        # belongs to which model
        model = User
        # included fields
        fields = (
            "username",
            "email",
            "password",
        )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            "website",
            "picture",
        )
