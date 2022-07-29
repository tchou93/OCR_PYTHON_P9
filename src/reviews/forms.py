from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms

from reviews.models import Review, Ticket


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {"headline": "Titre de la critique",
                  "rating": "Note",
                  "body": "Commentaire"
                  }
        CHOICES = [(0, '- 0'),
                   (1, '- 1'),
                   (2, '- 2'),
                   (4, '- 3'),
                   (4, '- 4'),
                   (5, '- 5')
                   ]
        widgets = {"rating": forms.RadioSelect(choices=CHOICES)}



class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {"title": "Titre",
                  "description": "Description",
                  "image": "Image"}

# class TicketForm(forms.ModelForm):
#     title = forms.CharField(
#         label="Title",
#         max_length=128,
#         widget=forms.TextInput()
#     )
#     description = forms.CharField(
#         label="Description",
#         max_length=2048,
#         widget=forms.Textarea(),
#         required=False
#     )
#     image = forms.ImageField(
#         label="Image",
#         required=False
#     )
#
#     class Meta:
#         model = Ticket
#         fields = ['title', 'description', 'image']

# class UserRegisterForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password1', 'password2']
#
#
# class SubscriptionForm(forms.Form):
#     followed_user = forms.CharField(
#         label=False,
#         widget=forms.TextInput()
#     )
