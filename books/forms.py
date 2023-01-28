from django import forms
from django.utils.text import slugify

from django_summernote.widgets import SummernoteWidget

from .models import Category, Genre, Author, Book, Review, Recommendation


class AuthorForm(forms.ModelForm):
    """
    A form for adding an author.
    """
    class Meta:
        model = Author
        fields = '__all__'


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
                    'class': 'form-select', 'required': False}),
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'desc': 'Description',
            'lang': 'Language',
            'pub_date': 'Publication Date'
        }
        help_texts = {
            'genre': 'Please fill in the Add a New Genre field below if \
                the genre has not been listed.',
            'author': 'To choose multiple authors, hold down Control(Windows) \
                or Command(Mac) and select authors. Please click + to \
                    add an author that has not been listed.'}

    new_genre = forms.CharField(
        max_length=254,
        required=False,
        label='Add a New Genre')
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
        'discount_rate']

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

    def clean(self):
        # Validate the genre/new_genre input and save it.
        category = self.cleaned_data.get('category')
        genre = self.cleaned_data.get('genre')
        new_genre = self.cleaned_data.get('new_genre')
        if not genre and not new_genre:
            raise forms.ValidationError('Please specify the genre in either \
                Genre or Add a New Genre field.')
        elif not genre:
            genre, created = Genre.objects.get_or_create(name=new_genre)
            self.cleaned_data['genre'] = genre
            genre.name = slugify(genre)
            genre.category = category
            genre.save()
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


class RecommendationForm(forms.ModelForm):
    """
    A form to allow the admin to post the book of the month session.
    """
    class Meta:
        model = Recommendation
        exclude = ('created_at',)
        widgets = {'content': SummernoteWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        books = Book.objects.all()
        book_list = [(book.id, book.title) for book in books]
        book_list.insert(0, ('', 'Choose a book'))
        self.fields['book'].choices = book_list
        self.fields['published'].label = 'Publish now.'
        for field in ['book', 'featured_year', 'featured_month']:
            self.fields[field].widget.attrs.update({'class': 'form-select'})
