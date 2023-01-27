from books.models import Category, Genre


def sort_genres(request):
    """
    Return a list of genre names for each category.
    """
    genre_list = Genre.objects.all()
    fiction_list = genre_list.filter(category__name='fiction')
    nonfiction_list = genre_list.filter(category__name='nonfiction')
    childrens_list = genre_list.filter(category__name='childrens')

    context = {
        'fiction_list': fiction_list,
        'nonfiction_list': nonfiction_list,
        'childrens_list': childrens_list
    }

    return context
