from django import forms
from .models import Category, Genre, Author, Book, Review


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
        help_texts = {
            'genre': 'Please fill in the Add a New Genre field below if the genre has not been listed.'}

    new_genre = forms.CharField(max_length=254, label='Add a New Genre')
    field_order = [
        'category',
        'genre',
        'new_genre',
        'title',
        'author',
        'desc',
        'cover_url',
        'cover',
        'price',
        'pages',
        'dimension_x',
        'dimension_y',
        'dimension_z',
        'lang',
        'publisher',
        'pub_date',
        'isbn10',
        'isbn13',
        'discount_rate',
        'amount_sold']

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

    def clean(self):
        genre = self.cleaned_data.get('genre')
        new_genre = self.cleaned_data.get('new_genre')
        if not genre and not new_genre:
            raise forms.ValidationError(
                'Please specify the genre in either Genre or New Genre field.')
        elif not genre:
            genre, created = Genre.objects.get_or_create(name=new_genre)
            self.cleaned_data['genre'] = genre
        return super().clean()


class ReviewForm(forms.ModelForm):
    """
    A form to allow users to rate and review books.
    """
    class Meta:
        model = Review
        fields = ('rating', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].label = 'Overall rating'
        self.fields['content'].label = False
        self.fields['rating'].widget.attrs.update({
            'type': 'number',
            'min': 1,
            'max': 5,
            'required': True
        })
        self.fields['content'].widget.attrs.update({
            'rows': 5,
            'placeholder': 'Add a written review'
        })
