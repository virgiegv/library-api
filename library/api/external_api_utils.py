import requests

GOOGLE_BOOKS_SOURCE = 'google'
LOCAL_DB_SOURCE = 'local'


async def get_google_books_search(
            title=None,
            subtitle=None,
            authors=None,
            categories=None,
            editor=None,
            published_date=None):

    fields = [subtitle, categories, editor, published_date]
    filtered_fields = list(filter(lambda field: field is not None, fields))

    if title:
        filtered_fields.append('intitle:'+title.replace(' ', '+'))

    if authors:
        filtered_fields.append('inauthor:' + authors.replace(' ', '+'))

    search = '+'.join(filtered_fields)

    url = f'https://www.googleapis.com/books/v1/volumes?q={search}'
    r = requests.get(url)

    return r.json()


async def get_google_book_by_id(book_id):
    url = f'https://www.googleapis.com/books/v1/volumes/{book_id}'
    book_data = requests.get(url)

    return book_data.json()

