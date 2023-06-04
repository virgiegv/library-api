import graphene


class Book(graphene.ObjectType):
    source = graphene.String()
    book_id = graphene.String()
    title = graphene.String()
    subtitle = graphene.String()
    authors = graphene.List(graphene.String)
    categories = graphene.List(graphene.String)
    editor = graphene.String()
    published_date = graphene.String()

    def __init__(self, source, book_id, title, subtitle, authors, categories, editor, published_date):
        self.source = source
        self.book_id = book_id
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.categories = categories
        self.editor = editor
        self.published_date = published_date

    @classmethod
    async def get_book(
            cls,
            title=None,
            subtitle=None,
            authors=None,
            categories=None,
            editor=None,
            published_date=None,
            any=None,
    ):
        import pdb

        book = cls(source='google', book_id='asdSD345Z', title='titulo', subtitle='jeje',
               authors=['stephenie meyer', 'jk rowling'],
               categories=['fiction', 'YA', 'adventure', 'fantasy', 'romance'], editor='god',
               published_date='2003-01-06')

        pdb.set_trace()
        return book


class Query(graphene.ObjectType):
    search = graphene.Field(
        Book,
        required=True,
        title=graphene.String(required=False),
        subtitle=graphene.String(required=False),
        authors=graphene.List(graphene.String, required=False),
        categories=graphene.List(graphene.String, required=False),
        editor=graphene.String(required=False),
        published_date=graphene.Date(required=False),
        any=graphene.String(required=False)
    )

    async def resolve_search(
            root,
            info,
            title=None,
            subtitle=None,
            authors=None,
            categories=None,
            editor=None,
            published_date=None,
            any=None
    ):
        return await Book.get_book(title, subtitle, authors, categories, editor, published_date, any)


schema = graphene.Schema(query=Query)
