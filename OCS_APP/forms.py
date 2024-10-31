from django import forms
from OCS_APP.models import ProductReview, Category, Manufacturer

class ProductFilterForm(forms.Form):
    manufacturer_choices = [('no-manu', 'Select Manufacturer')] + [(manu.id, manu.title) for manu in Manufacturer.objects.all()]
    category_choices = [('no-cat', 'Select Category')] + [(cat.id, cat.title) for cat in Category.objects.all()]

    manufacturer = forms.ChoiceField(choices=manufacturer_choices, required=False)
    category = forms.ChoiceField(choices=category_choices, required=False)

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget = forms.Textarea(attrs = {'placeholder':'Write your review..'}))
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']