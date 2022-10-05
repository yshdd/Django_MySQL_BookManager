from logging import PlaceHolder
from django import forms
from . import models
class FormForRental(forms.Form):
    stuid = forms.IntegerField(label="番号")
    stuname = forms.CharField(label="氏名")
    date = forms.DateField(
        label="日付",
        input_formats=['%Y-%m-%d'],
        widget=forms.widgets.DateInput(
            attrs={'placeholder':'YYYY-MM-DD'}
        )
        
        
    )
    book = forms.ModelChoiceField(
        queryset=models.Books.objects.filter(returned=True),
        label="書籍名"
    )

class FormForReturn(forms.Form):
    rentalid = forms.ModelChoiceField(
        queryset=models.LendBooks.objects.all(),
        label="貸出ID"
    )
    bookid = forms.ModelChoiceField(
        queryset=models.Books.objects.filter(returned=False),
        label="書籍名"
    )

class FormForUpdate(forms.Form):
    rentalid = forms.ModelChoiceField(
        queryset=models.LendBooks.objects.all(),
        label="貸出ID"
    )

    stuid = forms.IntegerField(label="番号")
    stuname = forms.CharField(label="氏名")
    date = forms.DateField(
        label="日付",
        input_formats=['%Y-%m-%d'],
        widget=forms.widgets.DateInput(
            attrs={'placeholder':'YYYY-MM-DD'}
        )   
    )
    book = forms.ModelChoiceField(
        queryset=models.Books.objects.filter(returned=True),
        label="書籍名",
        empty_label="変更なし",
        required=False,
    )