import graphene
from asgiref.sync import sync_to_async

from graphql import GraphQLError

from api.book_db_utils import sync_book_delete, sync_book_create
from api.book_schema import BookSchema
from api.external_api_utils import get_google_book_by_id


class BookSchemaType(graphene.ObjectType):
    results = graphene.List(BookSchema)

    async def resolve_results(root, info):
        title = info.context['title']
        subtitle = info.context['subtitle']
        authors = info.context['authors']
        categories = info.context['categories']
        editor = info.context['editor']
        published_date = info.context['published_date']

        return await BookSchema.get_book(title, subtitle, authors, categories, editor, published_date)


class Query(graphene.ObjectType):
    search = graphene.Field(
        BookSchemaType,
        required=True,
        title=graphene.String(required=False),
        subtitle=graphene.String(required=False),
        authors=graphene.String(required=False),
        categories=graphene.String(required=False),
        editor=graphene.String(required=False),
        published_date=graphene.String(required=False),
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
    ):
        info.context['title'] = title
        info.context['subtitle'] = subtitle
        info.context['authors'] = authors
        info.context['categories'] = categories
        info.context['editor'] = editor
        info.context['published_date'] = published_date

        return BookSchemaType()


class CreateBook(graphene.Mutation):
    class Arguments:
        source = graphene.String()
        book_id = graphene.String()

    ok = graphene.Boolean()
    title = graphene.String()
    book_id = graphene.String()

    async def mutate(root, info, source, book_id):
        book_data = {}
        if source == 'google':
            book_data = await get_google_book_by_id(book_id)

        volume_info = book_data.get('volumeInfo', {})
        if volume_info == {}:
            return GraphQLError('Could not retrieve specified book from source')

        created_book = await sync_to_async(sync_book_create)(volume_info, book_id)

        return CreateBook(
            ok=True,
            title=created_book.title,
            book_id=created_book.id
        )


class DeleteBook(graphene.Mutation):
    class Arguments:
        book_id = graphene.String()

    deleted = graphene.Boolean()

    async def mutate(root, info, book_id):
        deleted = await sync_to_async(sync_book_delete)(book_id)
        num_deleted = deleted[0]
        import pdb
        pdb.set_trace()

        return DeleteBook(deleted=(num_deleted != 0))


class BookMutations(graphene.ObjectType):
    create_book = CreateBook.Field()
    delete_book = DeleteBook.Field()


schema = graphene.Schema(query=Query, mutation=BookMutations)
