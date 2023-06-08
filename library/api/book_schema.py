import graphene
from asgiref.sync import sync_to_async

from api.external_api_utils import get_google_books_search
from api.models import Book


class BookSchema(graphene.ObjectType):
    source = graphene.String()
    book_id = graphene.String()
    title = graphene.String()
    subtitle = graphene.String()
    authors = graphene.List(graphene.String)
    categories = graphene.List(graphene.String)
    editor = graphene.String()
    published_date = graphene.String()
    image = graphene.String()
    description = graphene.String()

    def __init__(self, source, book_id, title, subtitle, authors,
                 categories, editor, published_date, image, description):
        self.source = source
        self.book_id = book_id
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.categories = categories
        self.editor = editor
        self.published_date = published_date
        self.image = image
        self.description = description

    @classmethod
    def _get_book(cls, params):
        books_qs = Book.objects.filter(**params)
        results = []

        for book in books_qs:
            book_authors = list(book.authors.all().values_list('name', flat=True))
            book_categories = list(book.categories.all().values_list('title', flat=True))

            results.append(
                cls(
                    source='local', book_id=book.id, title=book.title, subtitle=book.subtitle,
                    authors=book_authors, categories=book_categories, editor=book.editor,
                    published_date=book.published_date, image=book.image, description=book.description
                )
            )

        return results

    @classmethod
    async def get_book(
            cls,
            title=None,
            subtitle=None,
            authors=None,
            categories=None,
            editor=None,
            published_date=None,
    ):

        params = {}

        if title:
            params['title__icontains'] = title
        if subtitle:
            params['subtitle__icontains'] = subtitle
        if authors:
            params['authors__name__icontains'] = authors
        if categories:
            params['categories__title__icontains'] = categories
        if editor:
            params['editor__icontains'] = editor
        if published_date:
            params['published_date__icontains'] = published_date

        results = await sync_to_async(cls._get_book)(params)

        if len(results) <= 0:
            request_info = await get_google_books_search(title, subtitle, authors, categories, editor, published_date)

            search_results = request_info.get('items', [])
            for item in search_results:
                volume_info = item.get('volumeInfo', {})

                book = cls(
                    source='google',
                    book_id=item.get('id', None),
                    title=volume_info.get('title', ''),
                    subtitle=volume_info.get('subtitle', ''),
                    authors=volume_info.get('authors', []),
                    categories=volume_info.get('categories', []),
                    published_date=volume_info.get('publishedDate', ''),
                    description=volume_info.get('description', ''),
                    editor=volume_info.get('editor', ''),
                    image=volume_info.get('imageLinks', {}).get('thumbnail', '')
                )
                results.append(book)

        return results
