from django import forms
from .models import Category, Genre, Author, Book


class BookForm(forms.ModelForm):
    """
    A form for adding a book to database from the front-end.
    """

    class Meta:
        model = Book
        exclude = ('amount_sold',)

        widgets = {
            'category': forms.Select(
                attrs={
                    'class': 'form-select'}),
            'genre': forms.Select(
                attrs={
                    'class': 'form-select'}),
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        genres = Genre.objects.all()
        category_friendly_names = [(category.id, category.friendly_name)
                                   for category in categories]
        genre_friendly_names = [(genre.id, genre.friendly_name)
                                for genre in genres]

        category_friendly_names.insert(0, ('', 'Choose a category'))
        genre_friendly_names.insert(0, ('', 'Choose a genre'))
        self.fields['category'].choices = category_friendly_names
        self.fields['genre'].choices = genre_friendly_names
        self.fields['desc'].label = 'Description'
        self.fields['lang'].label = 'Language'
        self.fields['pub_date'].label = 'Publication Date'
