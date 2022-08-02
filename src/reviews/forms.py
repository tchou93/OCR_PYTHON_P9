from django import forms
from reviews.models import Review, Ticket


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {"headline": "Titre",
                  "rating": "Note",
                  "body": "Commentaire"
                  }
        CHOICES = [(0, '- 0'),
                   (1, '- 1'),
                   (2, '- 2'),
                   (3, '- 3'),
                   (4, '- 4'),
                   (5, '- 5')
                   ]
        widgets = {
            "rating": forms.RadioSelect(choices=CHOICES)
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {"title": "Titre",
                  "description": "Description",
                  "image": "Image"}
